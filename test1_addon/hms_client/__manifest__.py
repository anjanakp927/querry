{
    "name": "HMS Client",
    "version": "14.0.0.0.0",
    "category": "HMS",
    "author": "Codelayer Technologies Pvt Ltd",
    "depends": ["base", "account", "contacts", "product", "stock", "hr", "hr_attendance",
                "purchase_request", "purchase_quotations", "product_field", "cl_hms_coa", "partner_multi_company",
                "stock_request", "qm_production_mis", "l10n_in_hsn", "product_multi_company"],

    "data": [
        'security/ir.model.access.csv',
    ],
    "installable": True,
}
