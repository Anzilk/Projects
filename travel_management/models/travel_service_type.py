from odoo import models, fields


class TravelServiceType(models.Model):
    _name = "travel.service.type"
    _description = "travel service type"

    name = fields.Char(string="Service")
    expiration = fields.Integer('Expiration Period')
