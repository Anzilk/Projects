# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Community Spreadsheet',

    'version': '15.0.0.0.1',

    'summary': 'Documents',

    'sequence': 10,

    'description': """ Community Spreadsheet """,

    'category': 'Hidden/Tools',

    'website': 'https://www.cybrosys.com',

    'images': [],

    'depends': ['community_document', 'base'],

    'data': [],

    'demo': [],

    'installable': True,

    'application': True,

    'auto_install': False,

    'assets': {

        'web.assets_backend': [
            '/community_spreadsheet/static/src/js/spreadsheet.js',
        ],
        'web.assets_qweb': [
            '/community_spreadsheet/static/src/xml/spreadsheet_template.xml',
        ],
    },

    'license': 'LGPL-3',
}
