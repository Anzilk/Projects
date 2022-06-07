# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools


class DocumentsDocuments(models.Model):
    _name = "document.document"
    _description = "Documents"
    _rec_name = 'attachment_name'

    attachment_name = fields.Char('Name')
    attachment = fields.Many2one('ir.attachment', string='Add Document')
    attachment_view = fields.Binary('Document', related='attachment.datas')
    type = fields.Selection([
        ('binary', 'File'),
        ('url', 'URL'),
        ('empty', 'Request'),
    ], string='Type', related='attachment.type')

    def spreadsheet(self):
        print('hi')

