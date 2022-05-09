{
    'name': "Stock Repair",
    'version': '15.0.1.0.0',
    'depends': ['base', 'stock', 'sale_management'],
    'category': 'Sales',
    'installable': True,
    'data': ['views/stock_repair_views.xml',
             'views/stock_repair_menu.xml',
             'security/ir.model.access.csv'],
}
