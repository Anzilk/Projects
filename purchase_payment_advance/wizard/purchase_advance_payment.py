from odoo import fields, models, _
from odoo.exceptions import UserError
import time


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
    count = fields.Integer(string='Order Count')
    amount = fields.Float('Down Payment Amount',
                          digits='Account',
                          help="The percentage of amount to be payed in"
                               " advance, taxes excluded.")
    currency_id = fields.Many2one('res.currency', string='Currency')
    fixed_amount = fields.Monetary('Down Payment Amount (Fixed)',
                                   help="The fixed amount to be payed in"
                                        " advance, taxes excluded.")
    # deposit_account_id = fields.Many2one("account.account",
    # string="Income Account", domain=[('deprecated', '=', False)],
    #     help="Account used for deposits")
    # deposit_taxes_id = fields.Many2many("account.tax",
    # string="Customer Taxes", help="Taxes used for deposits")

    # @api.onchange('advance_payment_method')
    # def _onchange_advance_payment_method(self):
    #     # print(self.advance_payment_method,"jk")
    #     # print(self.env.context.get('active_id'),"id")
    #     print(self.amount, "amount 1")
    #     amount = self.default_get(['amount']).get('amount')
    #     print(amount,"amount 2")

    # to get advance payment amount and name
    def _get_advance_details(self, order):
        # context = {'lang': order.partner_id.lang}
        if self.advance_payment_method == 'percentage':
            amount = order.amount_untaxed * self.amount / 100
            name = _("Down payment of %s%%") % (self.amount)
        else:
            amount = self.fixed_amount
            name = _('Down Payment')
        # del context

        return amount, name

    # if there is no product on settings then set a default one
    def _prepare_deposit_product(self):
        return {
            'name': 'Down payment',
            'type': 'service',
            'invoice_policy': 'order',
            'company_id': False,
        }

    # prepare purchase order lines
    def _prepare_po_line(self, order, amount):
        # print(amount,"amount")
        # context = {'lang': order.partner_id.lang}
        po_values = {
            'name': _('Down Payment: %s') % (time.strftime('%m %Y'),),
            'price_unit': amount,
            'product_qty': 0.0,
            'order_id': order.id,
            'product_uom': self.product_id.uom_id.id,
            'product_id': self.product_id.id,
            'sequence': order.order_line and order.order_line[-1].sequence + 1
                        or 10,
        }
        # del context
        return po_values

    # prepare invoice values for regular bill
    def _prepare_regular_invoice_values(self, order):
        # print(order.order_line,"lines")
        po_order_line = []
        for po_line in order.order_line:
            print(po_line.product_id.purchase_method, "45678")
            if po_line.product_id.purchase_method == 'receive':
                qty=po_line.qty_received
            else:
                qty = po_line.product_qty
            # print(qty,"qwerty")
            po_order_line.append((0, 0, {
                'name': po_line.name,
                'product_id': po_line.product_id,
                'price_unit': po_line.price_unit,
                'quantity': qty
            }))
            # print(po_order_line,"poookffmcx")
        vals = {
            'move_type': 'in_invoice',
            'invoice_origin': order.name,
            'partner_id': order.partner_id.id,
            'fiscal_position_id': (
                        order.fiscal_position_id or order.fiscal_position_id.get_fiscal_position(
                    order.partner_id.id)).id,
            'currency_id': order.currency_id.id,
            'invoice_payment_term_id': order.payment_term_id.id,
            'invoice_line_ids': po_order_line
        }
        return vals

    # prepare invoice values for down payment
    def _prepare_invoice_values(self, order, name, amount, po_line):
        invoice_vals = {
            'move_type': 'in_invoice',
            'invoice_origin': order.name,
            'partner_id': order.partner_id.id,
            'fiscal_position_id': (order.fiscal_position_id or order.fiscal_position_id.get_fiscal_position(order.partner_id.id)).id,
            'currency_id': order.currency_id.id,
            'invoice_payment_term_id': order.payment_term_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'price_unit': amount,
                'quantity': 1.0,
                'product_id': self.product_id.id,
                'product_uom_id': po_line.product_uom.id,

            })],
        }
        return invoice_vals

    def _create_invoice(self, order, po_line, amount):
        if (self.advance_payment_method == 'percentage' and self.amount <= 0.00) or (self.advance_payment_method == 'fixed' and self.fixed_amount <= 0.00):
            raise UserError(_('The value of the down payment amount must be positive.'))

        amount, name = self._get_advance_details(order)

        invoice_vals = self._prepare_invoice_values(order, name, amount, po_line)
        # print(invoice_vals,"invoice values")

        if order.fiscal_position_id:
            invoice_vals['fiscal_position_id'] = order.fiscal_position_id.id

        invoice = self.env['account.move'].with_company(order.company_id)\
            .sudo().create(invoice_vals).with_user(self.env.uid)
        invoice.message_post_with_view('mail.message_origin_link',
                    values={'self': invoice, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id)
        # print(invoice.message_post_with_view('mail.message_origin_link',
        #             values={'self': invoice, 'origin': order},
        #             subtype_id=self.env.ref('mail.mt_note').id),"12345")
        return invoice


    #button action create invoices
    def create_invoices(self):
        purchase_orders = self.env['purchase.order'].browse(
            self.env.context.get('active_id'))
        if self.advance_payment_method == 'delivered':
            # print(purchase_orders)
            purchase_orders.action_create_invoice()
        elif self.advance_payment_method == 'regular':
            print("hii")
            for record in purchase_orders:
                vals = self._prepare_regular_invoice_values(record)
                print(vals,"invoice vals")
                self.env['account.move'].create(vals)
        else:
            settings_product = self.env[
                                   'ir.config_parameter'].sudo().get_param(
                'product_id')
            # print(settings_product, "product")
            # create down payment product if necessary
            if settings_product is not False:
                 self.product_id = int(settings_product)
            else:
                # print(self.product_id )
                # print('hii')
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('product_id', self.product_id.id)
            purchase_line_obj = self.env['purchase.order.line']
            # print(purchase_line_obj,"hii")
            for order in purchase_orders:
                # print(order.id,"id")
                amount, name = self._get_advance_details(order)
                # print(amount, name, "advance details")
                if self.product_id.type != 'service':
                    raise UserError(
                        _("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                if self.product_id.invoice_policy != 'order':
                    raise UserError(
                        _('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))

                # print(self.product_id.name)
                # for line in order.order_line:
                po_line_values = self._prepare_po_line(order, amount)
                po_line = purchase_line_obj.create(po_line_values)
                invoice = self._create_invoice(order, po_line, amount)
                # print(invoice,"invoice2")
                # print(po_line.product_uom.id,"uom")
                # if self._context.get('open_invoices', False):
                # print(self._context.get('open_invoices', False), "hh")
                # print("hii")
                print(invoice.invoice_line_ids.ids, "invoice line")
                print(po_line,"poline")
                # to set related invoice lines to po invoice line
                po_line.invoice_lines = invoice.invoice_line_ids.ids
                return purchase_orders.action_view_invoice(invoice)
                # return {'type': 'ir.actions.act_window_close'}
                # return {'type': 'ir.actions.act_window_close'}

