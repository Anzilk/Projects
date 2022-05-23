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

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    is_advance_payment = fields.Boolean("advance Payment", readonly=True)
