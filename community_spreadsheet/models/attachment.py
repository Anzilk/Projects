from odoo import models, api
import xlrd
import csv
import base64
import xlsxwriter
from xlutils.copy import copy
import xlrd
import tempfile
import xlwt
import io
from django.http import HttpResponse
import pandas as pd
from openpyxl import load_workbook


class AttachmentSpreadsheet(models.Model):
    _inherit = 'ir.attachment'

    def get_doc_file_data(self, *args):
        attachment = self.env['ir.attachment'].search([('id', '=', args[0])])
        bin_data = base64.b64decode(attachment.datas)
        wb = xlrd.open_workbook(file_contents=bin_data)
        # sheet = wb.sheets()[0]
        for s in wb.sheets():
            values = []
            for row in range(s.nrows):
                col_value = []
                for col in range(s.ncols):
                    value = (s.cell(row, col).value)
                    try:
                        value = str(int(value))
                    except:
                        pass
                    col_value.append(value)
                values.append(col_value)
        return values

    @api.model
    def add_data_spreadsheet(self, f_value, doc_id, r_value=0, c_value=0, ):
        # print(f_value,"hj")
        # print(r_value,c_value,"row col")
        # print(doc_id)
        row_value = int(r_value) - 1
        col_value = int(c_value) - 1
        # print(r_value, c_value, "row col after")
        attachment = self.env['ir.attachment'].browse(doc_id)
        print(attachment,"attachment")
        print(attachment.datas, "type")
        print(attachment.store_fname, "filename")
        # print(type(attachment.datas),"type")
        bin_data = base64.b64decode(attachment.datas)
        print('bin_data', type(bin_data), bin_data)
        file_path = tempfile.gettempdir() + '/file.xls'
        # data = attachment.file_import
        # f = open(file_path, 'wb')
        # f.write(data.decode('base64'))
        # f.close()
        # print("filepath=", file_path)
        # workbook = xlrd.open_workbook(file_path)

        workbook_r = xlrd.open_workbook(file_contents=bin_data)
        print(workbook_r)
        sheet_r = workbook_r.sheet_by_index(0)
        print(sheet_r,"sheet r")
        workbook_w = copy(workbook_r)

        sheet_w = workbook_w.get_sheet(0)
        # print("sheet w ", sheet_w)
        sheet_w.write(row_value, col_value, f_value)
        workbook_w.save('/home/cybrosys/Downloads/Untitled 1.xlsx')

        # workbook_w.close()
        # data = io.BytesIO(sheet_w)
        # data_record = base64.b64encode(data)
        # print('data_record', data)

        # ir_values = {
        #     'name': attachment.name,
        #     'type': 'binary',
        #     'datas': data_record,
        #     'store_fname': data_record,
        #     'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        # }
        # attachment.write(ir_values)
        # output = io.BytesIO()
        # workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # sheet = workbook.add_worksheet()
        # cell_format = workbook.add_format({'font_size': '12px'})
        # head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        # txt = workbook.add_format({'font_size': '10px'})
        # sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
        # sheet.write('B6', 'From:', cell_format)
        # sheet.merge_range('C6:D6', data['start_date'], txt)
        # sheet.write('F6', 'To:', cell_format)
        # sheet.merge_range('G6:H6', data['end_date'], txt)
        # workbook.close()
        # output.seek(0)
        # response.stream.write(output.read())
        # output.close()

        # attachment = self.env['ir.attachment'].search([('id', '=', doc_id)])
        # bin_data = base64.b64decode(attachment.datas)
        # workbook = load_workbook('chart(1).xlsx')

        return True
