# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    min_rfq = fields.Boolean(string="Minimum RFQ", config_parameter='purchase_requests.min_rfq')
    min_rfq_count = fields.Integer(string="Minimum RFQ Count", config_parameter='purchase_requests.min_rfq_count')
