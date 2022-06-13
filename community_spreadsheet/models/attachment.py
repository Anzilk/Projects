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
            font_values = []
            for row in range(s.nrows):
                col_value = []
                italic_value = []
                for col in range(s.ncols):
                    font = wb.font_list

                    # a=(s.cell(row, col))
                    # print("cell.xf_index is", a.xf_index)
                    # fmt = wb.xf_list[a.xf_index]
                    # print("type(fmt) is", type(fmt))
                    value = (s.cell(row, col).value)
                    # size = s.cell(row, col).font.size
                    cell_xf = wb.xf_list[s.cell_xf_index(row, col)]
                    # print(font[cell_xf.font_index].__dict__,"format")
                    italic =font[cell_xf.font_index].italic
                    # print(font[cell_xf.font_index].italic,"format")
                    # print(value, "value")
                    # print(size,"fontsize")
                    # print("Dumped Info:")
                    # fmt.dump()
                    try:
                        value = str(int(value))
                    except:
                        pass
                    col_value.append(value)
                    italic_value.append(italic)
                values.append(col_value)
                font_values.append(italic_value)
                # print(values,"values")
                # print(font_values,"font values")
        return values, font_values

    @api.model
    def add_data_spreadsheet(self, f_value, doc_id, r_value=0, c_value=0, ):
        row_value = int(r_value) - 1
        # print(r_value, "r value is after")
        col_value = int(c_value) - 1
        # print(r_value, c_value, "row col after")
        attachment = self.env['ir.attachment'].browse(doc_id)
        # print(type(attachment.datas),"type")
        bin_data = base64.b64decode(attachment.datas)
        # f = open(file_path, 'wb')
        workbook_r = xlrd.open_workbook(file_contents=bin_data)
        sheet_r = workbook_r.sheet_by_index(0)
        workbook_w = copy(workbook_r)
        sheet_w = workbook_w.get_sheet(0)
        # style = workbook_w.add_format({'bold': True})
        # cell_format = workbook_w.add_format()
        # cell_format.set_bold()
        # style = xlwt.easyxf('font: bold 1')
        sheet_w.write(row_value, col_value, f_value)

        workbook_w.save(Path(Path.home(),'sampl.xls'))

        stp_file = Path(Path.home(), 'sampl.xls')
        stp_object_file = open(stp_file, 'rb')
        stp_object_file_encode = base64.b64encode(stp_object_file.read())
        stp_object_file_encode = stp_object_file_encode.decode('utf-8')
        attachment.write({'datas': stp_object_file_encode})

        return True
