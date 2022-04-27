from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TravelPackage(models.Model):
    _name = "travel.package"
    _description = "Travel Package"
    name = fields.Char('Name', required=True)
    package_customer = fields.Many2one("res.partner", 'Customer',
                                       required=True)
    quotation_date = fields.Date('Quotation Date')
    source_location_package_id = fields.Many2one("travel.location",
                                                 "Source Location",
                                                 required=True)
    destination_location_package_id = fields.Many2one("travel.location",
                                                      'Destination Location',
                                                      required=True)
    package_start_date = fields.Datetime('Start Date')
    travel_vehicle_id = fields.Many2one("travel.vehicle")
    package_end_date = fields.Datetime('End Date')
    number_of_travellers = fields.Integer("No. Of Travellers")
    facilities_id = fields.Many2one("travel.facilities", string="Facilities")
    package_vehicle_type = fields.Selection(selection=[
        ('bus', 'Bus'),
        ('traveller', 'Traveller'),
        ('van', 'Van'),
        ('other', 'Other')], string='Vehicle Type')
    vehicle_list_id = fields.Many2one("travel.vehicle", "Vehicle",
                                      required=True)
    vehicle_charge_line_ids = fields.One2many("package.vehicle.charge.line",
                                              "package_line_id")
    state = fields.Selection(string='State', default='draft',
                             selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed')])
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self:
                                  self.env.user.company_id.currency_id)
    total = fields.Float("Total", compute="compute_total")
    estimated_km = fields.Float(string='Estimated Km')
    service_package_id = fields.Many2one("travel.service.type",
                                         string='Service Package')

    # vehicle list based on domain
    @api.onchange('facilities_id', 'package_vehicle_type',
                  'package_start_date', 'package_end_date',
                  'number_of_travellers',)
    def on_change_package_vehicle(self):
        # print(self, "b")
        # print(self.facilities_id.name)
        # print(rec.number_of_travellers)
        return {'domain': {'vehicle_list_id': [
                ('vehicle_type', '=', self.package_vehicle_type),
                ('start_date', '<', self.package_start_date),
                ('end_date', '>', self.package_end_date),
                ('number_of_seats', '=', self.number_of_travellers),
                ('facility_ids', '=', self.facilities_id.name)]}}

    # lines from vehicle charges
    @api.onchange('vehicle_list_id')
    def on_change_vehicle(self):
        # print(self.vehicle_list_id.id, "s")
        record = self.env["travel.vehicle"].search([
            ('id', '=', self.vehicle_list_id.id)])
        # print(record)
        # print(record.line_ids)
        vals = []
        for line in record.line_ids:
            # print("p", line.amount)
            # print(self.vehicle_charge_line_ids.amount)
            vals.append((0, 0, {
                    'package_service_id': line.vehicle_service_id,
                    'quantity': line.quantity,
                    'unit_id': line.unit_id,
                    'amount': line.amount,
            }))
        self.write({'vehicle_charge_line_ids': [(5, 0)]})
        self.write({'vehicle_charge_line_ids': vals})

# compute total
    @api.depends('vehicle_charge_line_ids.subtotal')
    def compute_total(self):
        # print(self)
        total = 0.0
        for record in self:
            for line in record.vehicle_charge_line_ids:
                total += line.subtotal
            record.total = total

# check vehicle already taken
#     @api.constrains('vehicle_list_id')
    def action_confirm(self):
        record = self.env["travel.package"].search([
            ('vehicle_list_id', '=', self.vehicle_list_id.id),
            ('package_end_date', '>=', self.package_start_date),
            ('package_start_date', '<=', self.package_end_date)])
        print(len(record))
        # # print(self.vehicle_list_id)
        if len(record) > 1:
            raise ValidationError("Vehicle Is Already Taken")
        else:
            # print("hi")
            record.state = "confirmed"
            vals = []
            for line in record.vehicle_charge_line_ids:
                # print(line.package_service_id)
                vals.append((0, 0, {
                    'estimation_service_id': line.package_service_id.id,
                    'quantity': line.quantity,
                    'amount': line.amount,
                }))
                # print(vals)

            # print(self.service_package_id)
            self.env['travel.management'].create({
                'customer_id': self.package_customer.id,
                'source_location_id': self.source_location_package_id.id,
                'destination_location_id':
                self.destination_location_package_id.id,
                'number_of_passengers': self.number_of_travellers,
                'travel_date': self.package_start_date,
                'service_id': self.service_package_id.id,
                'estimation_line_ids': vals,
                'estimated_km': self.estimated_km
            })


class PackageVehicleChargeLine(models.Model):
    _name = "package.vehicle.charge.line"
    _description = "Package Vehicle Charge Line"

    package_line_id = fields.Many2one("travel.package")
    package_service_id = fields.Many2one("product.template", string="Service")
    quantity = fields.Integer("Quantity")
    unit_id = fields.Many2one("uom.uom", "Unit")
    amount = fields.Float("Amount")
    package_line_currency_id = fields.Many2one('res.currency',
                                               string='Currency',
                                               default=lambda self:
                                               self.env.user.company_id.
                                               currency_id)
    subtotal = fields.Float("Subtotal", compute="compute_subtotal")

    @api.depends("amount", "quantity")
    def compute_subtotal(self):
        # print(self, "ww")
        for line in self:
            line.subtotal = line.quantity * line.amount

    @api.onchange('package_service_id')
    def on_change_vehicle_service(self):
        # print("hii")
        return {'domain': {'package_service_id': [
            ('detailed_type', '=', 'service')]}}
