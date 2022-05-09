from odoo import models, fields, api, _


class StockRepair(models.Model):
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
    product_id = fields.Many2one(
        "product.product", string="Product", required=True)
    customer_id = fields.Many2one("res.partner", string="Customer",
                                  readonly=True, save=True)

    # to set customer from sale order and show products only from its
    # corresponding sale order
    @api.onchange('sale_order_id')
    def onchange_sale_order_id(self):
        self.customer_id = self.sale_order_id.partner_id
        return {'domain': {'product_id': [
            ('id', '=', self.sale_order_id.order_line.product_id.ids)]}}

    # action  on  button
    def action_done(self):
        self.state = 'done'


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    is_repair = fields.Boolean(string="Repair", compute="_compute_repair")
    repair_id = fields.Many2one("stock.repair", string="Is Repair")

    # to check sale order have repair request
    @api.depends("repair_id.sale_order_id")
    def _compute_repair(self):
        # print("self", self)
        for rec in self:
            record = self.env["stock.repair"].search(
                [('sale_order_id', '=', rec.id)])
            # print(record)
            # print(len(record))
            if record:
                # print("hii")
                # print(rec)
                rec.write({'is_repair': True})
                # print(rec.is_repair)
            else:
                rec.write({'is_repair': False})

    # to check customer have any pending repair request
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        # print(self.partner_id)
        record = self.env["stock.repair"].search(
            [('customer_id', '=', self.partner_id.id)])
        # print(record)
        if record:
            # print("hii")
            res = {'warning': {
                'title': _('Warning'),
                'message': _('This user has some pending repair requests')}}
            return res
