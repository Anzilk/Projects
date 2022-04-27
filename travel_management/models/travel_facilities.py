from odoo import models, fields


class TravelFacilities(models.Model):
    _name = "travel.facilities"
    _description = "Travel Facilities"
    name = fields.Char('facility')
