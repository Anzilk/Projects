from odoo import models, fields, api
from datetime import datetime


class TravelVehicle(models.Model):
    _name = "travel.vehicle"
    _description = "Travel Vehicle"

    registration_number = fields.Char('Registration No.', required=True,
                                      default=" ")
    _sql_constraints = [
        ('registration_number_unique', 'unique(registration_number)',
         'Registration Number Already Exists!')
    ]

    vehicle_type = fields.Selection(selection=[('bus', 'Bus'),
                                               ('traveller', 'Traveller'),
                                               ('van', 'Van'),
                                               ('other', 'Other')],
                                    string='Vehicle Type', default="bus")
    name = fields.Char('Name', compute="compute_name", store=True)

# compute vehicle name
    @api.depends("registration_number", "vehicle_type")
    def compute_name(self):
        # print(self, "ww")
        for line in self:
            line.name = line.registration_number + line.vehicle_type

    number_of_seats = fields.Integer("No. Of Seats", default='1')
    facility_ids = fields.Many2many("travel.facilities", string="Facilities")
    line_ids = fields.One2many("travel.vehicle.line", "line_id")
    start_date = fields.Datetime("Start Date", default=datetime.now())
    end_date = fields.Datetime("End Date")


class TravelVehicleLine(models.Model):
    _name = "travel.vehicle.line"
    _description = "Travel Vehicle Line"

    line_id = fields.Many2one("travel.vehicle")
    vehicle_service_id = fields.Many2one("product.template", string="Service")
    quantity = fields.Integer("Quantity", default="1", readonly="True")
    unit_id = fields.Many2one("uom.uom", "Unit")
    amount = fields.Float("Amount")

    @api.onchange('vehicle_service_id')
    def on_change_vehicle_service(self):
        # print("hii")
        return {'domain': {'vehicle_service_id': [
            ('detailed_type', '=', 'service')]}}
