{
    'name': "Travel Management",
    'version': '15.0.1.0.0',
    'depends': ['base', 'uom', 'account', 'sale_management'],
    'category': 'Travel',
    'installable': True,
    'application': True,
    'data': [
        'views/travel_management_views.xml',
        'wizard/travel_management_report_wizard_view.xml',
        'reporting/travel_management_report.xml',
        'security/security_group.xml',
        'security/travel_manager_rule.xml',
        'security/ir.model.access.csv',
        'views/travel_management_menu.xml',
        'data/travel_booking_ref_data.xml',
        'data/travel_cron.xml', ],
    'assets': {
        'web.assets_backend': [
            'travel_management/static/src/js/action_manager.js',
        ],
    },
}
