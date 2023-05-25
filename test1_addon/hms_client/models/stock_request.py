import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class StockRequestCreateAPI(models.Model):
    _name = 'stock_request.api.create'

    @api.model
    def action_create_stock_request(self, vals):
        stock_vals = {}
        stock_picking_list = []

        if 'request_by' in vals:
            request_by = int(vals.get('request_by'))
            stock_vals.update({'request_by': request_by or False})

        if 'request_date' in vals:
            request_date = vals.get('request_date')
            stock_vals.update({'request_date': request_date or False})

        if 'company_id' in vals:
            company_id = int(vals.get('company_id', False))
            stock_vals.update({'company_id': company_id or False})

        if 'operating_unit_id' in vals:
            operating_unit_id = int(vals.get('operating_unit_id', False))
            stock_vals.update({'operating_unit_id': operating_unit_id or False})

        if 'request_lines' in vals:
            request_lines = vals.get('request_lines')
            request_lines_pos = 0
            request_line_det = []

            for request_lines_item in request_lines:
                stock_vals_line_items = {}
                _logger.info("Service API : Purchase Details (%s)", request_lines_item)

                stock_vals_line_items.update({'product_id': int(request_lines_item['product_id'])})
                stock_vals_line_items.update({'product_qty': float(request_lines_item['product_qty'])})
                stock_vals_line_items.update({'product_uom_id': int(request_lines_item['product_uom_id'])})

                request_line_det.append((0, request_lines_pos, stock_vals_line_items))
                request_lines_pos = request_lines_pos + 1

            _logger.info("Service API :Request Lines Details (%s)", request_line_det)
            stock_vals.update({"stock_request_line_ids": request_line_det})

        stock_request = self.env['stock.request'].create(stock_vals)
        if stock_request:
            _logger.info("Service API : issue Indent Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'stock_request_id': str(stock_request.id),
            })


class StockIssueAPI(models.Model):
    _name = 'stock_issue.api'

    @api.model
    def action_create_stock_issue(self, vals):
        stock_vals = {}

        if 'date' in vals:
            date = (vals.get('date'))
            stock_vals.update({'date': date or False})

        if 'stock_request_id' in vals:
            stock_request_id = (vals.get('stock_request_id'))
            stock_vals.update({'stock_request_id': stock_request_id or False})

        if 'operating_unit_id' in vals:
            operating_unit_id = int(vals.get('operating_unit_id'))
            stock_vals.update({'operating_unit_id': operating_unit_id or False})

        if 'warehouse_id' in vals:
            warehouse_id = int(vals.get('warehouse_id'))
            stock_vals.update({'ware_house': warehouse_id or False})

        if 'request_by' in vals:
            request_by = int(vals.get('request_by'))
            stock_vals.update({'request_by': request_by or False})

        if 'issued_by' in vals:
            issued_by = int(vals.get('issued_by'))
            stock_vals.update({'issued_by': issued_by or False})

        if 'company_id' in vals:
            company_id = int(vals.get('company_id', False))
            stock_vals.update({'company_id': company_id or False})

        if 'stock_lines' in vals:
            stock_lines = vals.get('stock_lines')
            issue_lines_pos = 0
            issue_line_det = []
            for request_lines_item in stock_lines:
                stock_vals_line_items = {}
                _logger.info("Service API : Issue Details (%s)", request_lines_item)

                stock_vals_line_items.update({'product_id': int(request_lines_item['product_id'])})
                stock_vals_line_items.update({'product_qty': float(request_lines_item['product_qty'])})
                product = self.env['product.product'].browse(int(request_lines_item['product_id']))
                stock_vals_line_items.update({'product_uom_id': product.uom_id.id})
                stock_vals_line_items.update({'location_id': int(request_lines_item['location_id'])})
                if 'analytic_account_id' in request_lines_item:
                    stock_vals_line_items.update({'analytic_account_id': int(request_lines_item['analytic_account_id'])})
                stock_location = self.env['stock.location'].search(
                    [('id', '=', int(request_lines_item['location_id']))])
                stock_vals_line_items.update({'warehouse_id': stock_location.get_warehouse().id})

                issue_line_det.append((0, issue_lines_pos, stock_vals_line_items))
                issue_lines_pos = issue_lines_pos + 1

            _logger.info("Service API :Issue Lines Details (%s)", issue_line_det)
            stock_vals.update({"stock_issue_line_ids": issue_line_det})
        stock_issue = self.env['stock.issue'].create(stock_vals)
        if stock_issue:
            if stock_issue.stock_request_id:
                stock_issue.action_approve()
                stock_issue.action_confirm()
                _logger.info("Service API : issue Indent Created")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'stock_issue_id': str(stock_issue.id),
                    'stock_delivery_id': str(stock_issue.stock_picking_id.id),

                })

