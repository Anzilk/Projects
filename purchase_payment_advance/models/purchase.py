from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_invoice(self):
        return {
            'name': 'Create Bill',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'purchase.advance.payment',
            'target': 'new'
        }
