# -*- coding: utf-8 -*-

{
    'name': 'Purchase Quotation',
    'category': 'Purchase',
    'version': '13.0.0.0',
    'sequence': 1,
    'description': """  Odoo Purchase Quotation   """,
    'depends': [
        'purchase','stock','product_field'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        # 'report/purchase_quotation_views.xml',
        'views/purchase_quotation_views.xml',
        'views/purchase_order_views.xml',
        'views/quotation_revision_views.xml',
        # 'report/purchase_quotation_report_template.xml',
        # 'report/purchase_quotation_report.xml',

    ],
    'qweb': [
    ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}