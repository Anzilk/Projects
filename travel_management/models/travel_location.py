from odoo import models, fields


class TravelLocation(models.Model):
    _name = "travel.location"
    _description = "Travel Location"
    name = fields.Char('Location')
