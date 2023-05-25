import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class StockReceiptCreateAPI(models.Model):
    _name = 'receipt.api.create'

    @api.model
    def action_create_receipt(self, vals):
        receipt_vals = {}
        purchase_order = False
        # warehouse = self.env['stock.warehouse'].browse(int(vals.get('warehouse_id')))

        if 'receipt_id' in vals:
            receipt_id = int(vals.get('receipt_id'))

        if 'stock_lines' in vals:
            stock_lines = (vals.get('stock_lines'))
            receipt_vals.update({'stock_lines': stock_lines})

        if 'company_id' in vals:
            company_id = (vals.get('company_id'))
            receipt_vals.update({'company_id': company_id})

        # if 'operating_unit_id' in vals:
        #     operating_unit_id = (vals.get('operating_unit_id'))
        #     receipt_vals.update({'operating_unit_id': operating_unit_id})

        stock_picking = self.env['stock.picking'].browse(int(vals.get('receipt_id')))
        if stock_picking:
            purchase_order = stock_picking.purchase_id.id
            if stock_picking.state != 'done':
                stock_picking.action_confirm()
                stock_picking.action_assign()

                for sl in vals.get('stock_lines'):
                    for move_line in stock_picking.move_lines:
                        product_id = int(sl['product_id'])
                        if product_id == move_line.product_id.id:
                            if move_line.product_uom_qty > 0 and move_line.quantity_done == 0:
                                move_line.write({"quantity_done": sl['quantity_done']})
                            else:
                                move_line.unlink()
                stock_picking._action_done()

                if 'create_bill' in vals:
                    create_bill = (vals.get('create_bill'))
                    if create_bill == 'T':
                        stock_picking.purchase_id.action_create_invoice()

                back_order = self.env['stock.picking'].search([('backorder_id', '=', int(vals.get('receipt_id')))])
                _logger.info("Service API : Receipt Created")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "Receipt Created",
                    'picking_id': str(stock_picking.id),
                    'back_order': str(back_order.id) if back_order else 0,
                    'purchase_order_id': str(purchase_order) if purchase_order else 0,
                })
            else:
                back_order = self.env['stock.picking'].search([('backorder_id', '=', int(vals.get('receipt_id')))])
                _logger.info("Service API : Receipt already Created")
                status = 'REJECTED'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': 'Receipt already Created',
                    'picking_id': str(stock_picking.id),
                    'purchase_order_id': str(purchase_order) if purchase_order else 0,
                    'back_order': str(back_order.id) if back_order else 0,
                })
