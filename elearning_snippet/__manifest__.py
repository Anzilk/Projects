{
    'name': 'E-learning Snippet',
    'category': 'Website/Website',
    'version': '15.0.1.0.0',
    'depends': ['website', 'website_sale', 'website_slides' ],
    'installable': True,
    'data': ['views/elearning_snippet.xml'],
    'assets': {
        'web.assets_frontend': [
            'elearning_snippet/static/src/js/e_learning.js',
        ],
    }
}
