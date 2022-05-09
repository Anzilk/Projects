
from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


three_months_after = datetime.now() + relativedelta(months=3)


class EstateModel(models.Model):
    _name = "estate.property"
    _description = "estate"
    name = fields.Char('Title', required=True, translate=True)
    property_type = fields.Char('Property type', translate=True)
    post_code = fields.Char('Post code')
    date_availability = fields.Date('Available from ', copy=False,
                                    default=three_months_after)
    tags = fields.Char('Tags', translate=True)
    bedroom = fields.Integer('Bedroom', required=True, default=3)
    living_area = fields.Integer('Living area', required=True)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', default=100, readonly=True,
                                 copy=False)
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=True)
    garden_area = fields.Integer('Garden area',)
    garden_orientation = fields.Selection(string='Garden orientation',
                                          selection=[('west', 'west'),
                                                     ('east', 'east'),
                                                     ('north', 'north'),
                                                     ('south', 'south')],
                                          help="garden orientation is used to"
                                               " show the orientation of"
                                               "  garden ")
    active = fields.Boolean(active=True)
    state = fields.Selection(string='state',
                             selection=[('new', 'New'),
                                        ('offer received', 'Offer received'),
                                        ('offer accepted', 'Offer accepted'),
                                        ('sold', 'Sold'),
                                        ('canceled', 'Canceled')],
                             required=True, copy=False, default='new')
    properties_type = fields.Many2one("estate.property",
                                      string="property type")
    buyer = fields.Many2one("estate.property", string="Buyer")
    seller = fields.Many2one("estate.property", string="seller")
