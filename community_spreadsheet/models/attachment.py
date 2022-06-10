from odoo import models, api
import csv
import base64
from pathlib import Path
import codecs
import xlsxwriter
from xlutils.copy import copy
import xlrd
import tempfile
import xlwt
import io
from openpyxl.styles import Font
from django.http import HttpResponse
import pandas as pd
from openpyxl import load_workbook


class AttachmentSpreadsheet(models.Model):
    _inherit = 'ir.attachment'

    def get_doc_file_data(self, *args):
        print(type(args),args,"svv")
        attachment = self.env['ir.attachment'].search([('id', '=', args[0])])
        bin_data = base64.b64decode(attachment.datas)
        wb = xlrd.open_workbook(file_contents=bin_data, formatting_info=True)
        # sheet = wb.sheets()[0]
        for s in wb.sheets():
            values = []
            for row in range(s.nrows):
                col_value = []
                for col in range(s.ncols):
                    font = wb.font_list

                    # a=(s.cell(row, col))
                    # print("cell.xf_index is", a.xf_index)
                    # fmt = wb.xf_list[a.xf_index]
                    # print("type(fmt) is", type(fmt))
                    value = (s.cell(row, col).value)
                    # size = s.cell(row, col).font.size
                    cell_xf = wb.xf_list[s.cell_xf_index(row, col)]
                    print(font[cell_xf.font_index].__dict__,"format")
                    print(value, "value")
                    # print(size,"fontsize")
                    # print("Dumped Info:")
                    # fmt.dump()
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
        # print(type(doc_id),"doc_id")
        # print(r_value,"r value is")
        # print(r_value,"r value is after")
        row_value = int(r_value) - 1
        # print(r_value, "r value is after")
        col_value = int(c_value) - 1
        # print(r_value, c_value, "row col after")
        attachment = self.env['ir.attachment'].browse(doc_id)
        # print(type(attachment.datas),"type")
        bin_data = base64.b64decode(attachment.datas)
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
        print("sheet w ", sheet_w)
        print("workbook_w ", workbook_w)
        # style = workbook_w.add_format({'bold': True})

        # style = xlwt.easyxf('font: bold 1')
        sheet_w.write(row_value, col_value, f_value)
        # print("dec bin data",sheet_w,"type=",type(sheet_w))
        # sheet = base64.b64decode(sheet_w)
        # print("decoded sheet" ,sheet)

        workbook_w.save(Path(Path.home(),'sampl.xlsx'))

        stp_file = Path(Path.home(), 'sampl.xlsx')
        stp_object_file = open(stp_file, 'rb')
        stp_object_file_encode = base64.b64encode(stp_object_file.read())
        stp_object_file_encode = stp_object_file_encode.decode('utf-8')
        # print(content,"new content")
        # a = base64.b64encode(bin_data)
        # print("a",a)
        attachment.write({'datas': stp_object_file_encode})
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
