# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    request_id = fields.Many2one('purchase.request', string='Purchase Request')
    hms_purchase_req_id = fields.Char(string='HMS PURCHASE REQ ID')
    _sql_constraints = [
        ('hms_purchase_req_id_unique', 'unique(hms_purchase_req_id)', _(" ID already exist!")),
    ]

