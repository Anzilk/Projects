from odoo import models, fields
from odoo.exceptions import ValidationError


class ToleranceTolerance(models.Model):
    _inherit = "res.partner"

    tolerance = fields.Float("Tolerance")

    _sql_constraints = [
            ('check_tolerance', 'CHECK(tolerance >= 0 AND tolerance <= 100)',
             'The Percentage Of Tolerance Should Be Between 0 And 100.')
        ]


class SaleTolerance(models.Model):
    _inherit = "sale.order.line"

    tolerance = fields.Float(string="Tolerance",
                             related='order_id.partner_id.tolerance',
                             readonly=False)


class PurchaseTolerance(models.Model):
    _inherit = "purchase.order.line"

    tolerance = fields.Float(string="Tolerance",
                             related='order_id.partner_id.tolerance',
                             readonly=False)


class TransferTolerance(models.Model):
    _inherit = "stock.move"

    tolerance = fields.Float(string="Tolerance",
                             related='picking_id.partner_id.tolerance',
                             readonly=False)


class TransferTolerancePicking(models.Model):
    _inherit = "stock.picking"

# check tolerance is out of range
    def button_validate(self):

        for rec in self.move_ids_without_package:
            # print(rec.tolerance - rec.product_uom_qty)

            for line in self.move_line_ids_without_package:
                # print(self.move_line_ids_without_package.qty_done)
                if line.qty_done\
                        < rec.product_uom_qty - rec.tolerance  \
                        or line.qty_done\
                        > rec.product_uom_qty + rec.tolerance:
                    raise ValidationError("Tolerance Is Out Of Range")
                    # ctx = {
                    #         'default_model': 'stock.picking',
                    #         'mark_so_as_sent': True,
                    #         }
                    # return {
                    #     'name': 'Warning',
                    #     'type': 'ir.actions.act_window',
                    #     'view_mode': 'form',
                    #     'res_model': 'tolerance.tolerance.wizard',
                    #     'target': 'new',
                    #
                    # }

        transfer = super(TransferTolerancePicking, self).button_validate()
        return transfer
