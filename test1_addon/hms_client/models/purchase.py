import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


# class PurchaseRequestCreateAPI(models.Model):
#     _name = 'purchase.request.api.create'
#
#     @api.model
#     def action_purchase_request_create(self, vals):

class purchaseCreateAPI(models.Model):
    _name = 'purchasee.api.create'

    @api.model
    def action_purchasee(self, vals):

        drilling_vals = {}

        purchase_request_vals = {}

        if 'purchase_req_id' in vals:
            purchase_req_id = int(vals.get('purchase_req_id'))

        if 'event_type' in vals:
            event_type = (vals.get('event_type'))

        if 'date_start' in vals:
            date_start = (vals.get('date_start'))
            purchase_request_vals.update({'date_start': date_start or False})

        if 'company_id' in vals:
            company_id = int(vals.get('company_id', False))
            purchase_request_vals.update({'company_id': company_id or False})

        if 'requested_by' in vals:
            requested_by = int(vals.get('requested_by', False))
            purchase_request_vals.update({'requested_by': requested_by or False})

        if 'assigned_to' in vals:
            assigned_to = int(vals.get('assigned_to', False))
            purchase_request_vals.update({'assigned_to': assigned_to or False})

        if 'description' in vals:
            description = (vals.get('description', False))
            purchase_request_vals.update({'description': description or False})

        if 'origin' in vals:
            origin = (vals.get('origin', False))
            purchase_request_vals.update({'origin': origin or False})

        if 'reason' in vals:
            reason = (vals.get('reason', False))
            purchase_request_vals.update({'reason': reason or False})

        # if 'operating_unit_id' in vals:
        #     operating_unit_id = int(vals.get('operating_unit_id', False))
        #     purchase_request_vals.update({'operating_unit_id': operating_unit_id or False})

        if 'quotation_lines' in vals:
            purchase_request = {}
            quotation_line = vals.get('quotation_lines')
            _logger.info("Service API : Purchase Request Details (%s)", purchase_request)
            purchase_request_pos = 0
            purchase_request_line_det = []

            for purchase_request_item in quotation_line:
                purchase_request_line_items = {}

                purchase_request_line_items.update({'product_id': int(purchase_request_item['product_id'])})
                purchase_request_line_items.update({'name': str(purchase_request_item['description'])})
                purchase_request_line_items.update({'product_qty': float(purchase_request_item['product_qty'])})
                purchase_request_line_items.update({'date_required': str(purchase_request_item['date_required'])})
                purchase_request_line_items.update({'estimated_cost': float(purchase_request_item['estimated_cost'])})

                purchase_request_line_det.append((0, purchase_request_pos, purchase_request_line_items))
                purchase_request_pos = purchase_request_pos + 1
            _logger.info("Service API :Purchase Lines Details (%s)", purchase_request_line_det)
            purchase_request_vals.update({"line_ids": purchase_request_line_det})

        if event_type == 'create':
            purchase_request_id = self.env['purchase.request'].create(purchase_request_vals)
            if purchase_request_id:
                _logger.info("Service API : Purchase Request Created")
                if 'is_approved' in vals:
                    is_approved = (vals.get('is_approved'))
                    if is_approved == 'T':
                        purchase_request_id.button_to_approve()
                        purchase_request_id.button_approved()
                        if purchase_request_id.state == 'approved':
                            _logger.info("Service API : Purchase Request Approved")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'purchase_request_id': purchase_request_id.id,
                    'request_status': purchase_request_id.state
                })

        if event_type == 'approve':
            purchase_request_id = self.env['purchase.request'].browse(int(vals.get('purchase_req_id')))
            if purchase_request_id:
                purchase_request_id.button_to_approve()
                purchase_request_id.button_approved()
                if purchase_request_id.state == 'approved':
                    _logger.info("Service API : Purchase Request Approved")
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'purchase_request_id': purchase_request_id.id,
                        'request_status': purchase_request_id.state
                    })
                else:
                    _logger.info("Service API : Purchase Request Not Approved or in another state")
                    status = 'REJECTED'
                    status_code = 404
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'purchase_request_id': purchase_request_id.id,
                        'request_status': purchase_request_id.state
                    })

        if event_type == 'cancel':
            quotation_line = self.env['purchase.quotation'].search(
                [('request_id', '=', int(vals.get('purchase_req_id')))])
            if quotation_line:
                _logger.info(
                    "Service API : Purchase Request cannot be cancelled, Purchase Quotation already created,  (%s)",
                    vals.get('purchase_req_id'))
                status = 'REJECTED'
                status_code = 404
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'purchase_request_id': vals.get('purchase_req_id'),
                    'request_status': ''
                })
            else:
                purchase_request_id = self.env['purchase.request'].browse(int(vals.get('purchase_req_id')))
                if purchase_request_id:
                    purchase_request_id.button_rejected()
                    _logger.info("Service API : Purchase Request Cancelled (%s )", purchase_request_id.id)
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'purchase_request_id': purchase_request_id.id,
                        'request_status': purchase_request_id.state
                    })


class PurchaseOrderCreateAPI(models.Model):
    _name = 'purchase.order.api.create'

    @api.model
    def action_purchase_order_create(self, vals):

        purchase_order_vals = {}

        if 'request_id' in vals:
            request_id = int(vals.get('request_id'))
            purchase_order_vals.update({'request_id': request_id or False})

        if 'purchase_order_id' in vals:
            purchase_order_id = int(vals.get('purchase_order_id'))

        if 'event_type' in vals:
            event_type = (vals.get('event_type'))

        if 'date_order' in vals:
            date_order = (vals.get('date_order'))
            purchase_order_vals.update({'date_order': date_order or False})

        if 'receipt_date' in vals:
            receipt_date = (vals.get('receipt_date'))
            purchase_order_vals.update({'receipt_date': receipt_date or False})

        if 'company_id' in vals:
            company_id = int(vals.get('company_id', False))
            purchase_order_vals.update({'company_id': company_id or False})

        if 'partner_id' in vals:
            partner_id = int(vals.get('partner_id', False))
            purchase_order_vals.update({'partner_id': partner_id or False})

        if 'user_id' in vals:
            user_id = int(vals.get('user_id', False))
            purchase_order_vals.update({'user_id': user_id or False})

        if 'picking_type_id' in vals:
            picking_type_id = int(vals.get('picking_type_id', False))
            purchase_order_vals.update({'picking_type_id': picking_type_id or False})

        if 'payment_term_id' in vals:
            payment_term_id = int(vals.get('payment_term_id', False))
            purchase_order_vals.update({'payment_term_id': payment_term_id or False})

        if 'fiscal_position' in vals:
            fiscal_position = int(vals.get('fiscal_position', False))
            purchase_order_vals.update({'fiscal_position': fiscal_position or False})

        if 'incoterm_id' in vals:
            incoterm_id = int(vals.get('incoterm_id', False))
            purchase_order_vals.update({'incoterm_id': incoterm_id or False})

        if 'partner_ref' in vals:
            partner_ref = (vals.get('partner_ref', False))
            purchase_order_vals.update({'partner_ref': partner_ref or False})

        if 'hms_purchase_mode' in vals:
            hms_purchase_mode = (vals.get('hms_purchase_mode', False))
            purchase_order_vals.update({'hms_purchase_mode': hms_purchase_mode or False})

        if 'warehouse_id' in vals:
            warehouse = self.env['stock.warehouse'].browse(int(vals.get('warehouse_id')))
            purchase_order_vals.update({'picking_type_id': warehouse.in_type_id.id})

        if 'operating_unit_id' in vals:
            operating_unit_id = int(vals.get('operating_unit_id', False))
            purchase_order_vals.update({'operating_unit_id': operating_unit_id or False})
            purchase_order_vals.update({'requesting_operating_unit_id': operating_unit_id or False})

        if 'order_lines' in vals:
            order_lines = vals.get('order_lines')
            _logger.info("Service API : Purchase Order Details (%s)")
            purchase_order_pos = 0
            purchase_order_line_det = []

            for purchase_order_item in order_lines:
                purchase_order_line_items = {}

                purchase_order_line_items.update({'product_id': int(purchase_order_item['product_id'])})
                purchase_order_line_items.update({'name': str(purchase_order_item['description'])})
                purchase_order_line_items.update({'product_qty': float(purchase_order_item['product_qty'])})
                purchase_order_line_items.update({'product_uom': int(purchase_order_item['product_uom'])})
                purchase_order_line_items.update({'price_unit': float(purchase_order_item['price_unit'])})
                if 'taxes_id' in purchase_order_item:
                    tax_ids = []
                    tax_string = purchase_order_item['taxes_id']
                    _logger.info("Service API : Taxes String %s", tax_string)
                    if tax_string:
                        tax_list = tax_string.split(',')
                        for tax_id in tax_list:
                            tax_ids.append(int(tax_id))
                        _logger.info("Service API : Tax Id List %s", tax_ids)
                        purchase_order_line_items.update({'taxes_id': [(6, 0, tax_ids or [])]})
                purchase_order_line_det.append((0, purchase_order_pos, purchase_order_line_items))
                purchase_order_pos = purchase_order_pos + 1
            _logger.info("Service API :Purchase Lines Details (%s)", purchase_order_line_det)
            purchase_order_vals.update({"order_line": purchase_order_line_det})

        if event_type == 'create':
            purchase_request = self.env['purchase.request'].browse(request_id)
            print(purchase_request)
            if purchase_request.state == 'approved' or purchase_request.state == 'done':
                print(purchase_request.state)
                purchase_orderid = self.env['purchase.order'].create(purchase_order_vals)
                if purchase_orderid:
                    if 'is_approved' in vals:
                        is_approved = (vals.get('is_approved'))
                        if is_approved == 'T':
                            purchase_orderid.button_confirm()
                            _logger.info("Service API : Purchase Order Created")
                            status = 'SUCCESS'
                            status_code = 200
                            return json.dumps({
                                'status': status,
                                'status_code': status_code,
                                'purchase_order_id': purchase_orderid.id,
                                'order_status': str(purchase_orderid.state),
                                'receipt_id': purchase_orderid.picking_ids.id,

                            })
                        else:
                            _logger.info("Service API : Purchase Order Created")
                            status = 'SUCCESS'
                            status_code = 200
                            return json.dumps({
                                'status': status,
                                'status_code': status_code,
                                'purchase_order_id': purchase_orderid.id,
                                'order_status': str(purchase_orderid.state),
                                'receipt_id': purchase_orderid.picking_ids.id,

                            })
            else:
                _logger.info("Service API : Purchase Request is not Approved")
                status = 'FAILED'
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'purchase_order_id': None,
                    'order_status': "Purchase Request is not Approved",
                    'receipt_id': None,

                    })
        if event_type == 'approve':
            purchase_order = self.env['purchase.order'].search([('id', '=', vals.get('purchase_order_id'))])
            if purchase_order:
                purchase_order.button_confirm()
                _logger.info("Service API : Purchase Request Approved (%s )", purchase_order.id)
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'purchase_order_id': purchase_order.id,
                    'order_status': str(purchase_order.state),
                    'receipt_id': purchase_order.picking_ids.id,

                })

        if event_type == 'cancel':
                purchase_orderid = self.env['purchase.order'].search(
                    [('id', '=', vals.get('purchase_order_id'))])
                if purchase_orderid:
                    purchase_orderid.button_cancel()
                    _logger.info("Service API : Purchase Request Cancelled (%s )", purchase_orderid.id)
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'purchase_order_id': purchase_orderid.id,
                        'order_status': str(purchase_orderid.state),
                        'receipt_id': purchase_orderid.picking_ids.id,

                    })
