import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class PurchaseQuotationCreateAPI(models.Model):
    _name = 'purchase.quotation.api.create'

    @api.model
    def action_create_purchase_quotation(self, vals):

        partner_vals = {}
        purchase_id = None

        if 'partner_id' in vals:
            partner_id = int(vals.get('partner_id'))
            partner_vals.update({'partner_id': partner_id or False})

        if 'company_id' in vals:
            company_id = int(vals.get('company_id', False))
            partner_vals.update({'company_id': company_id or False})

        if 'date_quotation' in vals:
            date_quotation = (vals.get('date_quotation', False))
            partner_vals.update({'date_quotation': date_quotation or False})

        if 'quotation_lines' in vals:
            purchase_quotation = {}
            quotation_line = vals.get('quotation_lines')
            _logger.info("Service API : Purchase Details (%s)", purchase_quotation)
            purchase_quotation_pos = 0
            purchase_quotation_line_det = []

            for purchase_quotation_item in quotation_line:

                purchase_quotation_line_items = {}
                _logger.info("Service API : Purchase Details (%s)", purchase_quotation_item)

                if 'taxes_id' in purchase_quotation:
                    taxes_id = []
                    tax_string = purchase_quotation_item['taxes_id']
                    _logger.info("Service API : Taxes String %s", tax_string)
                    if tax_string:
                       tax_list = tax_string.split(',')
                       for tax_id in tax_list:
                          taxes_id.append(int(tax_id))
                       _logger.info("Service API : Tax Id List %s", taxes_id)
                       purchase_quotation_line_items.update({'taxes_id': [(6, 0, taxes_id or [])]})
                purchase_quotation_line_items.update({'product_id': int(purchase_quotation_item['product_id'])})
                purchase_quotation_line_items.update({'product_qty':float(purchase_quotation_item['product_qty'])})
                purchase_quotation_line_items.update({'price_unit': float(purchase_quotation_item['price_unit'])})
                purchase_quotation_line_items.update({'name': str(purchase_quotation_item['description'])})

                purchase_quotation_line_det.append((0, purchase_quotation_pos, purchase_quotation_line_items))
                purchase_quotation_pos = purchase_quotation_pos + 1

            _logger.info("Service API :Purchase Lines Details (%s)", purchase_quotation_line_det)
            partner_vals.update({"quotation_line": purchase_quotation_line_det})
            purchase_id = self.env['purchase.quotation'].create(partner_vals)
            if purchase_id:
                _logger.info("Service API : purchase_id Created")
                status = 'SUCCESS'

                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                })
