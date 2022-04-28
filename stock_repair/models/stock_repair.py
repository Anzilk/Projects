from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ScrapSourceLocation(models.Model):
    _name = "stock.repair"
    _inherit = 'mail.thread'
    _description = "Stock Repair"
    _rec_name = 'sale_order_id'

    sale_order_id = fields.Many2one("sale.order", string="Sale Order",
                                    domain="[('state', '=', 'sale')]",
                                    required=True)
    state = fields.Selection(string='State', default='draft',
                             selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed'),
                                        ('done', 'Done')])
    product_id = fields.Many2one("product.product", string="Product")
    customer = fields.Char(string="Customer",
                           related='sale_order_id.partner_id.name')

    # to check customer have any pending request
    @api.onchange('sale_order_id')
    def on_change_product_id(self):
        # print("hii")
        # print(self.sale_order_id.id)
        # print(self.sale_order_id.order_line.product_id.ids)
        # print(self.customer)
        records = self.env["stock.repair"].search([('customer', '=',
                                                    self.customer),
                                                   ('state', '!=', 'done')])
        if len(records) >= 1:
            print(records)
            raise ValidationError("This user has some pending repair requests")
        return {'domain': {'product_id': [
            ('id', '=', self.sale_order_id.order_line.product_id.ids)]}}

    # action  on  button
    def action_done(self):
        self.state = 'done'


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    repair = fields.Boolean(string="Repair", compute="_compute_repair")
    is_repair = fields.Many2one("stock.repair", string="Is Repair")

    @api.depends("is_repair.sale_order_id")
    def _compute_repair(self):
        # print("self", self.id)

        record = self.env["stock.repair"]\
            .search([('sale_order_id', '=', self.id)])
        # print(record)
        # print(len(record))
        if len(record) > 0:
            # print("hii")
            self.write({'repair': True})
            print(self.repair)
        else:
            self.write({'repair': False})
