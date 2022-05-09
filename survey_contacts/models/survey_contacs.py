from odoo import models, fields


class SurveyContacts(models.Model):
    _name = "survey.contacts"
    _description = "Survey Contacts"

    survey_contact_id = fields.Many2one("survey.survey")
    question_id = fields.Many2one("survey.question", string="Questions",
                                  domain="[('survey_id', '=', parent.id)]")
    # contact_fields = fields.Selection(string=' Contact Fields',
    #                                   selection=[('name', 'name'),
    #                                              ('phone', 'phone'),
    #                                              ('mobile', 'mobile'),
    #                                              ('email', 'email'),
    #                                              ('website', 'website'),
    #                                              ])
    contact_fields_id = fields.Many2one(
        "ir.model.fields", string="Contact Fields",
        domain="[('model_id', '=', 'Contact')]")


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    survey_contact_ids = fields.One2many(
        "survey.contacts", "survey_contact_id")
