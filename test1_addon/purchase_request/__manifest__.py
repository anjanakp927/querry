{
    "name": "Purchase Request",
    "author": "",
    "version": "14.0.0.0.0",
    "sequence": 1.0,
    "summary": "Use this module to have notification of requirements of "
               "materials and/or external services and keep track of such "
               "requirements.",
    "website": "",
    "license": "",
    "category": "Purchase Management",
    "depends": ["purchase_quotations"],
    "data": [
        "security/purchase_request.xml",
        "security/ir.model.access.csv",
        "data/purchase_request_sequence.xml",
        # "data/purchase_request_data.xml",
        # "reports/report_purchase_request.xml",
        "wizard/purchase_request_line_make_purchase_order_view.xml",
        "wizard/purchase_request_rfq_wizard_views.xml",
        "views/purchase_request_views.xml",
        "views/res_config_settings_views.xml",
        "views/purchase_request_line_view.xml",
        "views/purchase_request_report.xml",
        "views/purchase_quotation_views.xml",
        # "views/product_template.xml",
        # "views/purchase_order_view.xml",
        # "views/stock_move_views.xml",
        # "views/stock_picking_views.xml",
    ],
    "demo": [
        "demo/purchase_request_demo.xml"
    ],
    "installable": True,
    "application": True,
}
