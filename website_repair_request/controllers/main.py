from odoo import http
from odoo.http import request


class ServiceRequest(http.Controller):
    @http.route(['/request'], type='http', auth="public", website=True)
    def service_request(self):
        products = request.env['product.product'].search([])
        customers = request.env['res.partner'].search([])
        # print("sdjk")
        values = {
            'products': products,
            'customers': customers
        }
        # print(values)
        return request.render(
            "website_repair_request.request_form", values)

    @http.route(['/succesful'], type='http', auth="public", website=True)
    def create_succesful(self, **kw):
        # print("jjk")
        print(kw)
        a = kw['product_id']
        # print(a)
        product = request.env['product.product'].search([('id', '=', a)])
        location = request.env['stock.location'].search([('id', '=', 8)])
        print(location.name)
        # print(product)
        # print(product.uom_id)
        kw['product_uom'] = product.uom_id.id
        kw['location_id'] = location.id
        # print(kw,"after")

        # for rec in  kw:
        # dict = {
        #     'partner_id': kw['partner_id'],
        #     'product_id': kw['product_id'],
        #     'product_qty': kw['product_qty'],
        #     'description': kw[description]
        # }



        request.env['repair.order'].sudo().create(kw)
        return request.render(
            "website_repair_request.request_succesful", {})
