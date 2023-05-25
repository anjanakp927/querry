# -*- coding: utf-8 -*-
{
    'name': "Product Fields",

    'summary': """additional fields in  product """,


    'description': """
        additional fields in  product
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Extra',
    'version': '0.1',
    'depends': ['purchase','stock','sale_management','uom'],
    'data': [
        'data/uom_data.xml',
        'views/product_field_view.xml',
        'views/res_config_settings_view.xml',
    ],

    'demo': [],
}
