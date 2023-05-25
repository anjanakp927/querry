# -*- coding: utf-8 -*-
{
    'name': "driver roster",

    'summary': """
        To assign each sales order to specific driver for service delivery""",
    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale', 'hr'],
    'data': [
        'data/sequence_data.xml',
        'security/ir.model.access.csv',
        'views/driver_roaster.xml',
    ],
    "auto_install": False,
    "installable": True,

}
