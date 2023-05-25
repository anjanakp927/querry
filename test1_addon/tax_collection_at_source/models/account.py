from odoo import fields, models, _


class AccountTax(models.Model):
    _inherit = 'account.tax'

    tcs = fields.Boolean('TCS', default=False)
    tcs_payment_excess = fields.Float('Payment in excess of')
    tcs_applicable = fields.Selection([('person', 'Individual'),
                                       ('company', 'Company'),
                                       ('common', 'Common')], string='Applicable to')
