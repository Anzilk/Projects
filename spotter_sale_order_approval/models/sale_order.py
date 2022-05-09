from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"
    state = fields.Selection(
        selection_add=[('first approval', 'First Approval'),
                       ('second approval', 'Second Approval'), ("sent",)],
        ondelete={'first approval': 'set default',
                  'second approval': 'set default'})
    is_first_approve = fields.Boolean(string="IS First Approve")
    is_second_approve = fields.Boolean(string="IS Second Approve")

    def action_quotation_send(self):
        sup = super(SaleOrder, self).action_quotation_send()
        print(self.amount_total)
        if self.amount_total >= 25000:
            self.is_first_approve = True
            return {
                'name': 'Warning',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'warning.wizard',
                'target': 'new'
            }
        return sup

    def action_submit(self):
        self.state = "first approval"

    def action_first_approval(self):
        self.is_second_approve = True
        self.state = "second approval"

    def action_second_approval(self):
        print('hii')
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def action_send_mail(self):
        sup = super(MailComposeMessage, self).action_send_mail()
        # print(self.env.context.get('default_model'), "123")
        active_id = self.env.context.get('active_id')
        record = self.env["sale.order"].browse(active_id)
        # print(record, "hii" )
        record.state = "sent"
        # record.action_quotation_sent()
        return sup
