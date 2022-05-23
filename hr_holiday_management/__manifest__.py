{
    'name': "Hr Holiday Management",
    'version': '15.0.1.0.0',
    'depends': ['base', 'hr_holidays', 'hr'],
    'category': 'hr/holidays',
    'installable': True,
    'data': ['security/ir.model.access.csv',
             'views/hr_leave_views.xml',
             'views/hr_leave_menu.xml'],
}
