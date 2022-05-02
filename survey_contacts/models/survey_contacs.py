from odoo import models, fields, api


class SurveyContacts(models.Model):
    _name = "survey.contacts"
    _description = "Survey Contacts"

    survey_contact_id = fields.Many2one("survey.survey")
    question_id = fields.Many2one("survey.question", string="Questions",
                                  domain="[('survey_id', '=', parent.id)]")
    contact_fields = fields.Selection(string=' Contact Fields',
                                      selection=[('name', 'name'),
                                                 ('phone', 'phone'),
                                                 ('mobile', 'mobile'),
                                                 ('email', 'email'),
                                                 ('website', 'website'),
                                                 ])

    # @api.onchange('question_id')
    # def on_change_question_id(self):
    #     print(self.question_id)
    #     print(self.survey_contact_id)
    #     print(self.survey_contact_id.id)
    #     print(self.survey_contact_id.title)
    #     active_id = self.env.context.get('active_ids')
    #     print(active_id, "1")
    #     # return {'domain': {'question_id': [
    #     #             ('survey_id', '=', self.survey_contact_id.id)]}}


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    survey_contact_ids = \
        fields.One2many("survey.contacts", "survey_contact_id")
