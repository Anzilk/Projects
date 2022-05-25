from odoo import fields, models, _
from odoo.exceptions import UserError
import time
from odoo.tools.float_utils import float_is_zero
from itertools import groupby


class PurchaseAdvancePaymentInv(models.TransientModel):
    _name = "purchase.advance.payment"
    _description = "Purchase Advance Payment Invoice"

    advance_payment_method = fields.Selection([
        ('regular', 'Regular bill'),
        ('delivered', 'Regular bill(deduct down payments)'),
        ('percentage', 'Down payment (percentage)'),
        ('fixed', 'Down payment (fixed amount)')
        ], string='Create Bill', default='delivered', required=True,
        help="A standard bill is issued with all the order lines ready"
             " for billing, according to their control policy "
             "(based on ordered or received quantity).")
    deduct_down_payments = fields.Boolean('Deduct down payments', default=True)
    has_down_payments = fields.Boolean('Has down payments', readonly=True)
    product_id = fields.Many2one('product.product',
                                 string='Down Payment Product',
                                 domain=[('type', '=', 'service')])
    amount = fields.Float('Down Payment Amount',
                          digits='Account',
                          help="The percentage of amount to be payed in"
                               " advance, taxes excluded.")
    currency_id = fields.Many2one('res.currency', string='Currency')
    fixed_amount = fields.Monetary('Down Payment Amount (Fixed)',
                                   help="The fixed amount to be payed in"
                                        " advance, taxes excluded.")

    # to get advance payment amount and name
    def _get_advance_details(self, order):
        if self.advance_payment_method == 'percentage':
            amount = order.amount_untaxed * self.amount / 100
            name = _("Down payment of %s%%") % (self.amount)
        else:
            amount = self.fixed_amount
            name = _('Down Payment')
        return amount, name

    # if there is no product on settings then set a default one
    def _prepare_deposit_product(self):
        return {
            'name': 'Down payment',
            'type': 'service',
             'purchase_method': 'purchase',
            'company_id': False,
        }

    # prepare purchase order lines
    def _prepare_po_line(self, order, amount):
        po_values = {
            'name': _('Down Payment: %s') % (time.strftime('%m %Y'),),
            'price_unit': amount,
            'product_qty': 0.0,
            'order_id': order.id,
            'product_uom': self.product_id.uom_id.id,
            'taxes_id': self.product_id.supplier_taxes_id,
            'product_id': self.product_id.id,
            'sequence':
                order.order_line and order.order_line[-1].sequence + 1 or 10,
            'is_advance_payment': True
        }
        return po_values

    # prepare invoice values for down payment
    def _prepare_invoice_values(self, order, name, amount, po_line):
        invoice_vals = {
            'move_type': 'in_invoice',
            'invoice_origin': order.name,
            'partner_id': order.partner_id.id,
            'fiscal_position_id': (order.fiscal_position_id or
                                   order.fiscal_position_id.get_fiscal_position
                                   (order.partner_id.id)).id,
            'currency_id': order.currency_id.id,
            'invoice_payment_term_id': order.payment_term_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'price_unit': amount,
                'quantity': 1.0,
                'product_id': self.product_id.id,
                'product_uom_id': po_line.product_uom.id,
                'tax_ids': [(6, 0, po_line.taxes_id.ids)],

            })],
        }
        return invoice_vals

    # create invoice for downpayment invoice
    def _create_invoice(self, order, po_line):
        if (self.advance_payment_method == 'percentage'
            and self.amount <= 0.00) or (
                self.advance_payment_method == 'fixed'
                and self.fixed_amount <= 0.00):
            raise UserError(_('The value of the down payment amount '
                              'must be positive.'))

        amount, name = self._get_advance_details(order)
        invoice_vals = self._prepare_invoice_values(order, name, amount,
                                                    po_line)
        if order.fiscal_position_id:
            invoice_vals['fiscal_position_id'] = order.fiscal_position_id.id

        invoice = self.env['account.move'].with_company(order.company_id)\
            .sudo().create(invoice_vals).with_user(self.env.uid)
        invoice.message_post_with_view('mail.message_origin_link',
                                       values={'self': invoice, 'origin': order
                                               },
                                       subtype_id=self.env.ref('mail.mt_note'
                                                               ).id)
        return invoice

    # button action create invoices
    def create_invoices(self):
        purchase_orders = self.env['purchase.order'].browse(
            self.env.context.get('active_id'))
        if self.advance_payment_method == 'delivered':
            deducted_regular_invoice = purchase_orders.action_create_invoice()
            if self._context.get('open_invoices', False):
                return deducted_regular_invoice
        elif self.advance_payment_method == 'regular':
            regular_invoice = self.regular_invoice(purchase_orders)
            if self._context.get('open_invoices', False):
                return purchase_orders.action_view_invoice(regular_invoice)
        else:
            settings_product = self.env[
                                   'ir.config_parameter'].sudo().get_param(
                'product_id')
            if settings_product is not False:
                self.product_id = int(settings_product)
            else:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param(
                    'product_id', self.product_id.id)
            purchase_line_obj = self.env['purchase.order.line']
            for order in purchase_orders:
                amount, name = self._get_advance_details(order)
                if self.product_id.type != 'service':
                    raise UserError(
                        _("The product used to invoice a down payment should"
                          " be of type 'Service'. Please use another product"
                          " or update this product."))
                if self.product_id.purchase_method != 'purchase':
                    raise UserError(
                        _('The product used to invoice a down payment '
                          'should have an invoice policy set to "Ordered'
                          ' quantities". Please update your deposit product to'
                          ' be able to create a deposit invoice.'))
                po_line_values = self._prepare_po_line(order, amount)
                po_line = purchase_line_obj.create(po_line_values)
                invoice = self._create_invoice(order, po_line)
                # to set related invoice lines to po invoice line
                po_line.invoice_lines = invoice.invoice_line_ids.ids
                if self._context.get('open_invoices', False):
                    return purchase_orders.action_view_invoice(invoice)

    # to create the regular bill
    def regular_invoice(self, orders):
        """Create the invoice associated to the PO.
        """
        # 1) Prepare invoice vals and clean-up the section lines
        invoice_vals_list = []
        for order in orders:
            if order.invoice_status != 'to invoice':
                continue
            order = order.with_company(order.company_id)
            # Invoice values.
            invoice_vals = self._prepare_regular_invoice(order)
            invoiceable_lines = self._get_invoiceable_lines(order)
            # Invoice line values (keep only necessary sections).
            for line in invoiceable_lines:
                res = {
                    'display_type': line.display_type,
                    'sequence': line.sequence,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom.id,
                    'quantity': line.qty_to_invoice,
                    'price_unit': line.price_unit,
                    'tax_ids': [(6, 0, line.taxes_id.ids)],
                    'analytic_account_id': line.account_analytic_id.id,
                    'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                    'purchase_line_id': line.id,
                }
                invoice_vals['invoice_line_ids'].append(
                        (0, 0, res))
            invoice_vals_list.append(invoice_vals)
        if not invoiceable_lines:
            raise UserError(
                _('There is no invoiceable line. '
                  'If a product has a control policy based on'
                  ' received quantity, please make sure that a quantity has'
                  ' been received.'))

        # 2) group by (company_id, partner_id, currency_id) for batch creation
        new_invoice_vals_list = []
        for grouping_keys, invoices in groupby(invoice_vals_list,
                                               key=lambda x: (
                                                       x.get('company_id'),
                                                       x.get('partner_id'),
                                                       x.get('currency_id'))):
            origins = set()
            payment_refs = set()
            refs = set()
            ref_invoice_vals = None
            for invoice_vals in invoices:
                if not ref_invoice_vals:
                    ref_invoice_vals = invoice_vals
                else:
                    ref_invoice_vals['invoice_line_ids'] += invoice_vals[
                        'invoice_line_ids']
                origins.add(invoice_vals['invoice_origin'])
                payment_refs.add(invoice_vals['payment_reference'])
                refs.add(invoice_vals['ref'])
            ref_invoice_vals.update({
                'ref': ', '.join(refs)[:2000],
                'invoice_origin': ', '.join(origins),
                'payment_reference': len(
                    payment_refs) == 1 and payment_refs.pop() or False,
            })
            new_invoice_vals_list.append(ref_invoice_vals)
        invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.
        moves = self.env['account.move']
        account_move = self.env['account.move'].with_context(
            default_move_type='in_invoice')
        for vals in invoice_vals_list:
            moves |= account_move.with_company(
                vals['company_id']).create(vals)
        # 4) Some moves might actually be refunds: convert them if the total
        # amount is negative
        # We do this after the moves have been created since we need taxes,
        # etc. to know if the total
        # is actually negative or not
        moves.filtered(
            lambda m: m.currency_id.round(
                m.amount_total) < 0
        ).action_switch_invoice_into_refund_credit_note()
        return moves

    # prepare values for regular invoice
    def _prepare_regular_invoice(self, order):
        """Prepare the dict of values to create the new invoice for a purchase
         order.
                """
        order.ensure_one()
        journal = self.env['account.move'].with_context(
            default_move_type='in_invoice')._get_default_journal()
        if not journal:
            raise UserError(
                _('Please define an accounting purchase journal for the'
                  ' company %s (%s).') % (
                    order.company_id.name, order.company_id.id))
        partner_invoice_id = order.partner_id.address_get(['invoice'])[
            'invoice']
        partner_bank_id = order.partner_id.bank_ids.filtered_domain(
            ['|', ('company_id', '=', False),
             ('company_id', '=', order.company_id.id)])[:1]
        invoice_vals = {
            'ref': order.partner_ref or '',
            'move_type': 'in_invoice',
            'narration': order.notes,
            'currency_id': order.currency_id.id,
            'invoice_user_id':
                order.user_id and order.user_id.id or self.env.user.id,
            'partner_id': partner_invoice_id,
            'fiscal_position_id': (
                        order.fiscal_position_id or
                        order.fiscal_position_id.get_fiscal_position(
                            partner_invoice_id)).id,
            'payment_reference': order.partner_ref or '',
            'partner_bank_id': partner_bank_id.id,
            'invoice_origin': order.name,
            'invoice_payment_term_id': order.payment_term_id.id,
            'invoice_line_ids': [],
            'company_id': order.company_id.id,
        }
        return invoice_vals

    # to get the po lines to invoice for a regular bill
    def _get_invoiceable_lines(self, order):
        """Return the invoiceable lines for order `self`."""
        invoiceable_line_ids = []
        pending_section = None
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for line in order.order_line:
            if line.display_type == 'line_section':
                # Only invoice the section if one of its lines is invoiceable
                pending_section = line
                continue
            if line.display_type != 'line_note' and float_is_zero(
                    line.qty_to_invoice, precision_digits=precision):
                continue
            if line.qty_to_invoice > 0 or line.display_type == 'line_note':
                if pending_section:
                    invoiceable_line_ids.append(pending_section.id)
                    pending_section = None
                invoiceable_line_ids.append(line.id)
        return self.env['purchase.order.line'].browse(invoiceable_line_ids)
