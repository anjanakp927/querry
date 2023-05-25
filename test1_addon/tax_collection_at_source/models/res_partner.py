

from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tcs_threshold_check = fields.Boolean(string='Check TCS Threshold', default=True)
    pan_no = fields.Char()
    turnover_check = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Total turnover in preceding financial year \
                                                                             exceeds Rs.10Crs')
    is_specified_person = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Is Specified Person')

