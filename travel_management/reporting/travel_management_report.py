from odoo import api, models
from datetime import datetime


class ReportTravelPackage(models.AbstractModel):
    _name = 'report.travel_management.report_travel_package'

    # create pdf report from abstract model
    @api.model
    def _get_report_values(self, docids, data=None):
        # docs = self.env['travel.management.report.wizard'].browse(docids)
        # print(data)
        # print(data['customer_id'])
        # print(data['date_from'])
        # print(self.date_from, "before")
        # print(self.date_to,"before date to=")
        if data['date_to'] is False:
            data['date_to'] = datetime.now()
        if data['date_from'] is not False:
            # print("hii not false")
            # print(self.date_to, "after date to")
            # print(data['date_from'], "after")
            # print(self.read()[0])
            # print(self.date_from, "from date")
            query = """SELECT l.name,d.name,p.state,v.name
                     FROM travel_package as p INNER JOIN travel_vehicle as v
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
            # print(records)
            records_list = []
            for rec in records:
                # print("my records",rec[0],rec[1],rec[2])
                vals = {
                    'source_location': rec[0],
                    'destination_location': rec[1],
                    'state': rec[2],
                    'vehicle': rec[3]
                }
                # print(vals,"my vals=")
                records_list.append(vals)
            # print(records_list)
            # print(self)
            # print(self.env.cr.dbname)

        else:
            # print("false code here")
            query = """SELECT l.name,d.name,p.state,v.name
                                FROM travel_package as p
                                 INNER JOIN travel_vehicle as v
                                 ON p.vehicle_list_id=v.id
                                 INNER JOIN travel_location as l
                                 ON p.source_location_package_id=l.id
                                 INNER JOIN travel_location as d
                                 ON p.destination_location_package_id=d.id
                                  WHERE package_end_date<='%s'
                                 AND package_customer='%s' """ \
                    % (data['date_to'], data['customer_id'])
            self._cr.execute(query)
            records = self.env.cr.fetchall()
            # print(records)
            records_list = []
            for rec in records:
                # print("my records",rec[0],rec[1],rec[2])
                vals = {
                    'source_location': rec[0],
                    'destination_location': rec[1],
                    'state': rec[2],
                    'vehicle': rec[3]
                }
                # print(vals,"my vals=")
                records_list.append(vals)
            # print(records_list)

        return {
              'doc_ids': docids,
              'doc_model': 'travel.management.report.wizard',
              'records': records_list,
              'data': data,

        }

    # def get_something(self):
    #     return 5
