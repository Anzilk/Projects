{
    'name': "Spotter Sale Order Approval",
    'version': '15.0.1.0.0',
    'depends': ['base', 'sale_management'],
    'category': 'Sales',
    'installable': True,
    'data': ['security/ir.model.access.csv',
             'security/spotter_sale_approval_group.xml',
             'wizard/sale_warning_wizard_views.xml',
             'views/spotter_sale_order_view.xml']
}
