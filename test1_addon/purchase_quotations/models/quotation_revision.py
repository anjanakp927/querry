# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from werkzeug.urls import url_encode

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang, get_lang


class PurchaseQuotationRevision(models.Model):
    _name = "purchase.quotation.revision"
    _description = "Quotation Revision"

    quotation_id = fields.Many2one('purchase.quotation', string='Purchase Quotation')
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

