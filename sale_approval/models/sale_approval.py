from odoo import models, fields
# from odoo.exceptions import UserError
# import warnings


class SaleApproval(models.Model):
    _inherit = "sale.order"

    is_send_to_manager = fields.Boolean("Send To Manager", default=True)
    state = fields.Selection(
        selection_add=[('waiting', 'Waiting For Approval'), ("sent",)],
        ondelete={'waiting': 'set default'})
    # type = fields.Selection(selection_add=[
    #                           ('waiting', 'Waiting For Approval')],
    #     ondelete={'waiting': 'set default'})

    # @api.model
    def action_quotation_send(self):
        sale = super(SaleApproval, self).action_quotation_send()
        # self.is_send_to_manager = False
        # print(self.order_line)
        for record in self.order_line:
            # print(record.price_unit)
            # print(record.product_template_id.list_price)
            # print(record.product_id.list_price, "t")
            new_price = record.price_unit
            unit_price = record.product_template_id.list_price
            if new_price != unit_price:
                # print("not match")
                self.is_send_to_manager = False
                # print(self.is_send_to_manager, "hii")
                # self.state = "draft"
                return {
                    'name': 'Warning',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'sale.warning.wizard',
                    'target': 'new'
                }
        return sale

#                # raise UserError("Need Approval From Manager")
#                # raise ValidationError("Need Approval From Manager")

    def action_send_to_manager(self):
        # print(self)
        self.state = "waiting"

    def action_approve(self):
        # print(self)
        # self.state = "sent"
        # if self.state == "sent":
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
        # return super(SaleApproval, self).action_quotation_send()

    def action_disapprove(self):
        # print(self,"aa")
        self.state = "draft"

        
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
