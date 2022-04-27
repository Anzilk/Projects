from odoo import models, api


class ScrapSourceLocation(models.Model):
    _inherit = "stock.scrap"

    @api.onchange('product_id')
    def on_change_product_id(self):
        print(self.product_id.id)
        r = self.env['stock.putaway.rule'].search([('product_id', '=', self.product_id.id)], limit=1)
        print(r.location_out_id.name)
        self.location_id = r.location_out_id
        # return {'domain': {'estimation_service_id': [
        #     ('detailed_type', '=', 'service')]}}

