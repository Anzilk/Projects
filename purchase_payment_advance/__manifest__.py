{
    'name': "Purchase Advance Payment",
    'version': '15.0.1.0.0',
    'depends': ['base', 'purchase', 'account'],
    'category': 'Sales',
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_advance_payment_views.xml',
        'views/res_config_settings_views.xml',
        'views/purchase_views.xml'],

}
