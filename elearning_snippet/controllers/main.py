from odoo import http
import time
from odoo.http import request


class Snippets(http.Controller):
    @http.route(['/elearning_snippet/elearning'],
                type='json', auth="public", website=True)
    def service_request(self, products_per_slide=4, **kwargs):
        records = request.env[
            'slide.channel'].search([], order='create_date desc')
        # print(records,"hii")
        records_grouped = []
        record_list = []
        for index, record in enumerate(records, 1):
            # print("recor",record)
            record_list.append(record)
            if index % products_per_slide == 0:
                records_grouped.append(record_list)
                record_list = []
        # print(record_list,"dd")
        if any(record_list):
            records_grouped.append(record_list)
            # print(records_grouped, "12")
        # for r in records_grouped:
        #     print(r)
        #     for y in r:
        #         print(y)
        # values = {'product': records}
        values = {
            "objects": records_grouped,
            "events_per_slide": products_per_slide,
            "num_slides": len(records_grouped),
            "uniqueId": "pc-%d" % int(time.time() * 1000),
        }
        response = http.Response(
            template='elearning_snippet.s_event_carousel_items',
            qcontext=values)
        return response.render()

        # return request.env['ir.ui.view']._render_template(
        #         'elearning_snippet.s_snippet_courses', values)

