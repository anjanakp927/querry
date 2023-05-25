import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class StockReturnCreateAPI(models.Model):
    _name = 'stock_return.api.create'

    @api.model
    def action_create_stock_return(self, vals):
        stock_vals = {}
        # warehouse = self.env['stock.warehouse'].browse(int(vals.get('warehouse_id')))

        if 'partner_id' in vals:
            partner_id = int(vals.get('partner_id'))
            stock_vals.update({'partner_id': partner_id or False})
            stock_vals.update({'return_type': "customer"})
            # stock_vals.update({'return_order': "customer"})

        if 'return_to_location' in vals:
            return_to_location = int(vals.get('return_to_location'))
            stock_vals.update({'return_to_location': return_to_location or False})

        return_from_location = self.env['stock.location'].search([('usage', '=', 'customer')], limit=1)
        stock_vals.update({'return_from_location': return_from_location.id})

        if 'company_id' in vals:
            company_id = (vals.get('company_id'))
            stock_vals.update({'company_id': company_id})

        if 'operating_unit_id' in vals:
            operating_unit_id = int(vals.get('operating_unit_id'))
            stock_vals.update({'operating_unit_id': operating_unit_id})

        if 'stock_lines' in vals:
            stock_lines = (vals.get('stock_lines'))
            stock_lines_pos = 0
            stock_line_det = []

            for stock_line_item in stock_lines:
                stock_return_line_items = {}

                stock_return_line_items.update({'product_id': int(stock_line_item['product_id'])})
                product = self.env['product.product'].browse(int(stock_line_item['product_id']))
                stock_return_line_items.update({'quantity': (stock_line_item['quantity'])})
                stock_return_line_items.update({'product_uom_id': product.uom_id.id})
                stock_line_det.append((0, stock_lines_pos, stock_return_line_items))
                stock_lines_pos = stock_lines_pos + 1

            stock_vals.update({"line_ids": stock_line_det})
        stock_return = self.env['stock.return.request'].create(stock_vals)
        if stock_return:
            stock_return.action_confirm()
            stock_return.action_validate()
            _logger.info("Service API : Stock Return Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'stock_return_id': str(stock_return.id),
                'stock_receipt_id': str(stock_return.returned_picking_ids.id),

            })
