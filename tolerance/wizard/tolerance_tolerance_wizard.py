from odoo import models, fields


class ToleranceToleranceWizard(models.TransientModel):
    _name = 'tolerance.tolerance.wizard'
    _description = 'Tolerance Tolerance wizard'
    name = fields.Text(default="Quantity Is Out Of Tolerance Range!",
                       store=True)

    def action_accept(self):
        # self.env['stock.picking'].browse(
        #     self.env.context.get('active_id')).button_validate()
        a = self.env['sale.order'].browse(
            self.env.context.get('active_id'))
        # a.state="done"
        # a.state = "draft"
        # a.write({'state': 'draft'})
        # print(a.state)
        print(a)
        return {
            'type': 'ir.actions.act_window_close'
        }

    def action_cancel(self):

        return {

            'type': 'ir.actions.act_window_close',
        }
