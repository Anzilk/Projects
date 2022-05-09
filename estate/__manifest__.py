{
    'name': "Real estate",
    'version': '1.0',
    'depends': ['base', 'uom'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    'installable': True,
    'application': True,
    'data': ['security/ir.model.access.csv',
             'views/estate_property_views.xml',
             'views/estate_menus.xml'],

}
