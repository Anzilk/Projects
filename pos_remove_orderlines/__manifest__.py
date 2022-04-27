{
    'name': "Pos Remove Lines",
    'version': '15.0.1.0.0',
    'depends': ['base', 'point_of_sale'],
    'category': 'Pos',
    'installable': True,
    'assets':
        {
            'point_of_sale.assets': [
                'pos_remove_orderlines/static/src/js/remove_orderlines.js',
                'pos_remove_orderlines/static/src/js/clear_all_orderlines.js'
            ],
            'web.assets_qweb': [
                'pos_remove_orderlines/static/src/xml/remove_lines.xml',
                'pos_remove_orderlines/static/src/xml/clear_all_orderline.xml'
            ],
        },
}
