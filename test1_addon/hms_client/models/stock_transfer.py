import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class StockTransferCreateAPI(models.Model):
    _name = 'stock_transfer.api.create'

    @api.model
    def action_create_stock_transfer(self, vals):
        stock_vals = {}
        # warehouse = self.env['stock.warehouse'].browse(int(vals.get('warehouse_id')))

        if 'partner_id' in vals:
            partner_id = int(vals.get('partner_id'))
            stock_vals.update({'partner_id': partner_id or False})

        if 'picking_type_id' in vals:
            picking_type_id = int(vals.get('picking_type_id'))
            stock_vals.update({'picking_type_id': picking_type_id or False})

        if 'location_id' in vals:
            location_id = int(vals.get('location_id'))
            stock_vals.update({'location_id': location_id or False})

        if 'location_dest_id' in vals:
            location_dest_id = int(vals.get('location_dest_id'))
            stock_vals.update({'location_dest_id': location_dest_id or False})

        if 'scheduled_date' in vals:
            scheduled_date = (vals.get('scheduled_date'))
            stock_vals.update({'scheduled_date': scheduled_date or False})

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
                stock_transfer_line_items = {}

                stock_transfer_line_items.update({'product_id': int(stock_line_item['product_id'])})
                product = self.env['product.product'].browse(int(stock_line_item['product_id']))
                stock_transfer_line_items.update({'product_uom_qty': ''})
                stock_transfer_line_items.update({'product_uom_id': product.uom_id.id})
                stock_transfer_line_items.update({'location_id': int(vals.get('location_id'))})
                stock_transfer_line_items.update({'location_dest_id': int(vals.get('location_dest_id'))})
                stock_line_det.append((0, stock_lines_pos, stock_transfer_line_items))
                stock_lines_pos = stock_lines_pos + 1
            _logger.info("Service API : Stock Lines Details (%s)", stock_line_det)
            stock_vals.update({"move_line_ids_without_package": stock_line_det})
        stock_transfer = self.env['stock.picking'].create(stock_vals)
        if stock_transfer:
            if stock_transfer.state != 'done':
                stock_transfer.action_confirm()
                stock_transfer.action_assign()
                for sl in vals.get('stock_lines'):
                    for move_line in stock_transfer.move_lines:
                        product_id = int(sl['product_id'])
                        if product_id == move_line.product_id.id:
                            if move_line.product_uom_qty > 0 and move_line.quantity_done == 0:
                                move_line.write({"quantity_done": sl['quantity_done']})
                stock_transfer._action_done()
                _logger.info("Service API : Stock Transfer Created")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'stock_transfer_id': str(stock_transfer.id),

                })
