{
    'name': "Sale Approval",
    'version': '15.0.1.0.0',
    'depends': ['base', 'sale_management'],
    'category': 'Sales',
    'installable': True,
    'data': ['views/sale_approval_views.xml',
             'wizard/sale_warning_wizard.xml',
             'security/sale_approval_security.xml',
             'security/ir.model.access.csv'],
}
