from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import json
import pytz
import io
from odoo.http import request
from odoo.tools import date_utils
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

one_months_after = datetime.now() + relativedelta(months=1)


class TravelManagementReportWizard(models.TransientModel):
    _name = 'travel.management.report.wizard'
    _description = 'Travel Management Report wizard'
    date_from = fields.Datetime(string="Date from", default=datetime.today())
    date_to = fields.Datetime(string="Date To", default=one_months_after)
    customer_id = fields.Many2one("res.partner", string="customer",
                                  required=True)

    def action_print(self):
        # print(self.customer_id,"dfr")
        if self.date_from is not False and self.date_to is not False:
            if self.date_from > self.date_to:
                raise ValidationError('Start Date must be less than End Date')
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'customer_id': self.customer_id.id,
            'customer_name': self.customer_id.name

        }
        return self.env.ref(
                'travel_management.action_travel_package').\
            report_action(self, data=data)

    # print xlsx report

    def action_print_xlsx(self):
        # print("hii its xlsx")
        if self.date_from is not False and self.date_to is not False:
            if self.date_from > self.date_to:
                raise ValidationError('Start Date must be less than End Date')

        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'customer_id': self.customer_id.id,
            'customer_name': self.customer_id.name

        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'travel.management.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        # print(response, "hii")
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # print(data)
        # print(data['date_to'])
        if data['date_to'] is False:
            data['date_to'] = one_months_after
        print(data['date_to'], "after")
        if data['date_from'] is not False:
            # print("hii not false")
            # print(self.date_to, "after date to")
            # print(data['date_from'], "after")
            # print(self.read()[0])
            # print(self.date_from, "from date")
            query = """SELECT l.name,d.name,p.state,v.name
                             FROM travel_package as p 
                             INNER JOIN travel_vehicle as v
                              ON p.vehicle_list_id=v.id
                              INNER JOIN travel_location as l
                              ON p.source_location_package_id=l.id
                              INNER JOIN travel_location as d
                              ON p.destination_location_package_id=d.id
                               WHERE package_start_date >='%s'
                              AND package_end_date<='%s'
                              AND package_customer='%s' """ \
                    % (data['date_from'], data['date_to'],
                       data['customer_id'])
            self._cr.execute(query)
            # print("execute=", self._cr.execute(query))
            # records = self._cr.dictfetchall()
            # print("records=", records)
            records = self.env.cr.fetchall()

        else:
            # print("false code here")
            query = """SELECT l.name,d.name,p.state,v.name
                                              FROM travel_package as p
                                               INNER JOIN travel_vehicle as v
                                               ON p.vehicle_list_id=v.id
                                               INNER JOIN travel_location as l
                                               ON p.source_location_package_id=
                                               l.id
                                               INNER JOIN travel_location as d
                                               ON p.destination_location_package_id=d.id
                                                WHERE package_end_date<='%s'
                                               AND package_customer='%s' """ \
                    % (data['date_to'], data['customer_id'])
            self._cr.execute(query)
            records = self.env.cr.fetchall()

        sheet = workbook.add_worksheet()
        sheet.set_column('B:N', 20)
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
        # txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('C2:F3', 'TRAVEL MANAGEMENT REPORT', head)
        sheet.write('B6', 'Date From:', cell_format)
        sheet.write('C6', data['date_from'], )
        sheet.write('B7', 'Date To:', cell_format)
        sheet.write('C7', data['date_to'], format2)
        sheet.write('B9', 'Sl No', cell_format)
        sheet.write('C9', 'Source Location', cell_format)
        sheet.write('D9', 'Destination Location', cell_format)
        sheet.write('E9', 'Vehicle Name', cell_format)
        sheet.write('F9', 'State', cell_format)
        row_number = 10
        index_num = 1
        for rec in records:
            sheet.write(row_number, 1, index_num)
            sheet.write(row_number, 2, rec[0])
            sheet.write(row_number, 3, rec[1])
            sheet.write(row_number, 4, rec[3])
            sheet.write(row_number, 5, rec[2])
            # print(rec)
            row_number += 1
            index_num += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
