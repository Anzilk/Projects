from odoo import models, fields, api
from datetime import datetime, timedelta
# from odoo.exceptions import UserError


class TravelManagement(models.Model):
    _name = "travel.management"
    _description = "Travel Management"

    name = fields.Char('Booking Ref', default=' ', readonly="1")

    # to create sequence number
    @api.model
    def create(self, vals):
        obj = super(TravelManagement, self).create(vals)
        # print(obj, "oooo")
        if obj.name == ' ':
            number = self.env['ir.sequence'].get('travel.booking.ref') or ' '
            obj.write({'name': number})
        return obj

    customer_id = fields.Many2one("res.partner", string='Customer')
    number_of_passengers = fields.Integer('No. Of Passengers', default=1)
    service_id = fields.Many2one("travel.service.type", string='Service')
    booking_date = fields.Date('Date ', default=datetime.now(),
                               help="Booking Date")
    source_location_id = fields.Many2one("travel.location",
                                         string="Source Location")
    destination_location_id = fields.Many2one("travel.location",
                                              string="Destination Location")
    travel_date = fields.Datetime("Travel Date")
    state = fields.Selection(string='State', default='draft',
                             selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed'),
                                        ('expired', 'Expired')])
    expiration_date = fields.Datetime('Expiration Date',
                                      compute="_compute_expiry_date")
    # is_package = fields.Boolean("Package", default=False)
    estimation_line_ids = fields.One2many("estimation.amount.line",
                                          "estimation_line_id")
    total = fields.Float("Total", compute="compute_total")
    currency_id = fields.Many2one('res.currency',
                                  string='Currency',
                                  default=lambda self:
                                  self.env.user.company_id.currency_id)
    estimated_km = fields.Float(string="Estimated Km")
    fees = fields.Float(string="Fees")
    payment_id = fields.Many2one('account.payment.term', string="Payment Term")
    today = fields.Date("Date", default=datetime.today())
    is_invoice = fields.Boolean("Invoice", default=True)
    company_id = fields.Many2one("res.company", "Company", readonly=True,
                                 default=lambda self:
                                 self.env['res.company']
                                 .browse(self.env['res.company']
                                         ._company_default_get(
                                     'travel.management')))
    current_user_id = fields.Many2one('res.users', 'Current User',
                                      default=lambda self: self.env.user,
                                      readonly=True)
    # user_id = fields.Many2one('res.users', 'Current User',
    #                           default=lambda self: self.env.user,
    #                           readonly=True)

    # @api.onchange('customer_id')
    # def on_change_customer_id(self):
    #     print(self.env.user.id)
    #     print(self.current_user_id.id)
    #     print(self.company_id.id)

    # compute total
    @api.depends('estimation_line_ids.subtotal')
    def compute_total(self):
        total = 0.0
        for record in self:
            for line in record.estimation_line_ids:
                total += line.subtotal
            record.total = total

    # compute expiration date
    @api.depends("service_id.expiration")
    def _compute_expiry_date(self):
        # print(self, "aa")
        for line in self:
            line.expiration_date = line.booking_date +\
                                   timedelta(days=line.service_id.expiration)

    # change state on click button
    def action_confirm(self):
        for record in self:
            record.state = "confirmed"
        return True

# change  state on expiry
    def expiry_checked(self):
        # print(self, "ll")
        date = datetime.now()
        records = self.env['travel.management']\
            .search([]).filtered(lambda x: x.expiration_date < date)
        # print(records, "rec")
        # print(self.expiration_date, "rec")
        for rec in records:
            rec.state = 'expired'
# print(rec.expiration_date)

# create invoice on button click
    def action_invoice(self):
        # print(self.service_id.id)
        # print(self.is_invoice, "before")
        self.is_invoice = False
        # print(self.is_invoice, "after")
        vals = []
        if self.service_id.id:
            # print(self.service_id.id,"hii")
            # print(self)
            for rec in self.estimation_line_ids:
                print(rec.amount)
                vals.append((0, 0, {
                    'product_id': rec.estimation_service_id,
                    'quantity': rec.quantity,
                    'price_unit': rec.amount,
                }))
        else:
            print(self.service_id)
            # self.service_id.name = "  "
            # print(self.service_id.name, "after")
            name = self.name
            vals.append((0, 0, {
                'name': name}))

        self.env['account.move'].create({
            'move_type': 'out_invoice',
            'date': datetime.today(),
            'partner_id': self.customer_id.id,
            'invoice_date': self.today,
            'currency_id': self.currency_id.id,
            'invoice_payment_term_id': self.payment_id.id,
            'payment_reference': self.name,
            'invoice_line_ids': vals
        })

    # @api.onchange('customer_id')
    # def on_change_vehicle_service(self):
    #     print(self.customer_id)

# invoice show on smart button
    def action_show_invoice(self):
        print(self)
        return {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'move_type': 'out_invoice',
            'domain': [('payment_reference', '=', self.name)],

        }

    # def write(self, vals):
    #     print(self.mapped('state'))
    #     if any(state == 'confirmed' for state in set(self.mapped('state'))):
    #         raise UserError("Can't Edit In Confirmed State")
    #     else:
    #         return super().write(vals)


class EstimationAmountLine(models.Model):
    _name = "estimation.amount.line"
    _description = "Estimation Amount Line"

    estimation_line_id = fields.Many2one("travel.management")
    estimation_service_id = fields.Many2one("product.template",
                                            string="Service")
    quantity = fields.Integer("Quantity")
    # unit_id = fields.Many2one("uom.uom", "Unit")
    amount = fields.Float("Amount")
    currency_id = fields.Many2one('res.currency',
                                  string='Currency',
                                  default=lambda self:
                                  self.env.user.company_id.currency_id)
    subtotal = fields.Float("Subtotal", compute="compute_subtotal")

    @api.depends("amount", "quantity")
    def compute_subtotal(self):
        # print(self, "ww")
        for line in self:
            line.subtotal = line.quantity * line.amount

# show only service products
    @api.onchange('estimation_service_id')
    def on_change_vehicle_service(self):
        # print("hii")
        # print(self)
        return {'domain': {'estimation_service_id': [
            ('detailed_type', '=', 'service')]}}
