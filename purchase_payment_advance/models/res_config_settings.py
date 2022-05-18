from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_id = fields.Many2one("product.product", string="Product",
                                 domain="[('detailed_type', '=', 'service')]")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        params = self.env['ir.config_parameter'].sudo()
        product = params.get_param('product_id', default=False)
        res.update(
            product_id=int(product),
        )
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("product_id",
                                                         self.product_id.id)
        return res
