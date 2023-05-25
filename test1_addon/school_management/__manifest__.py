# -*- coding: utf-8 -*-

{
    "name": "School Management System",
    "version": "14.0.1.1",
    'summary': "in this system we will get school management system ",
    "depends": ['base','purchase_stock'],
    "data": ["security/ir.model.access.csv",
             "views/school_views.xml",
             "report/student_report.xml",
             ],
    "demo": ["demo/school_demo_data.xml"],
    "auto_install": False,
    "installable": True,
    "price": 20,
    "currency": 'EUR',
    "category": "Accounting",
}
