from odoo import models, fields


class SaleWarningWizard(models.TransientModel):
    _name = 'sale.warning.wizard'
    _description = 'Sale Warning wizard'
    name = fields.Text(default="Need  Submit To Manager!", store=True)

    def action_close(self):
        return {
            'type': 'ir.actions.act_window_close'
        }
