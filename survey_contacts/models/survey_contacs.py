from odoo import models, fields


class SurveyContacts(models.Model):
    _name = "survey.contacts"
    _description = "Survey Contacts"

    survey_contact = fields.Many2one("survey.survey")
    question = fields.char(string="Questions")
    contact_fields = fields.Many2one("Contact Fields")
    # survey_contact_id = fields.Many2one("survey.survey")
    # question-id = fields.Many2one("survey.question")



