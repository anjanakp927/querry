import xmlrpc
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PurchaseRequestController(http.Controller):

    @http.route(['/purchasee'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_purchase_request_create(self, **post):
        print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")

        _logger.info("Service API : Data Received, Processing ......")

        status_code = 500
        status = "REJECTED"

        if not post:
            _logger.info("Service API : No Data Received or Incorrect Data Format!")
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': "No Data Received or Incorrect Data Format!",
            })

        _logger.info("Service API : Raw Data (JSON) Log Created")

        params = post.copy()

        _logger.info("Service API : Raw Data (JSON) copied")

        if params:
            if not params.get('username', False) \
                    or not params.get('password', False) \
                    :
                _logger.info("Service API : Login Parameters Not Available. Returning")
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "Missing Parameters",
                })

            user_id = request.env['res.users'].sudo().search([('login', '=', str(params['username']))],
                                                             limit=1)
            # user_id.update({'company_id':int(params['company_id'])})
            _logger.info("Service API : Company IDs of User (%s)  (%s)", user_id.name, user_id.company_ids)
            if not user_id:
                _logger.info('Service API : User Not Available Returning')
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred - User Not Available",
                })

            log_vals = {}

            if 'purchase_req_id' in params:
                purchase_req_id = int(params.get('purchase_req_id'))
                log_vals.update({'purchase_req_id': purchase_req_id or False})

            if 'is_approved' in params:
                is_approved = (params.get('is_approved'))
                log_vals.update({'is_approved': is_approved or False})

            if 'event_type' in params:
                event_type = (params.get('event_type'))
                log_vals.update({'event_type': event_type or False})

            if 'date' in params:
                date = (params.get('date'))
                log_vals.update({'date_start': date or False})

            if 'requested_by' in params:
                requested_by = (params.get('requested_by', False))
                log_vals.update({'requested_by': requested_by or False})

            if 'assigned_to' in params:
                assigned_to = (params.get('assigned_to', False))
                log_vals.update({'assigned_to': assigned_to or False})

            if 'description' in params:
                description = (params.get('description', False))
                log_vals.update({'description': description or False})

            if 'source_document' in params:
                origin = (params.get('source_document', False))
                log_vals.update({'origin': origin or False})

            if 'reason' in params:
                reason = (params.get('reason', False))
                log_vals.update({'reason': reason or False})

            # if 'operating_unit_id' in params:
            #     operating_unit_id = int(params.get('operating_unit_id', False))
            #     log_vals.update({'operating_unit_id': operating_unit_id or False})

            if 'quotation_lines' in params:
                quotation_lines = params.get('quotation_lines', False)
                log_vals.update({'quotation_lines': quotation_lines or False})

            if 'company_id' in params:
                company_id = int(params.get('company_id', False))
                log_vals.update({'company_id': company_id or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'purchasee.api.create',
                                                 'action_purchasee', [log_vals])
                    purchase_request_dict = json.loads(response)

                    status = 'SUCCESS'
                    status_code = 200
                    approved = False
                    return json.dumps({
                        'status': purchase_request_dict['status'],
                        'status_code': purchase_request_dict['status_code'],
                        'purchase_request_id': purchase_request_dict['purchase_request_id'],
                        'request_status': purchase_request_dict['request_status']

                    })

                except Exception as e:
                    status = "REJECTED"
                    status_code = 500
                    _logger.info("Service API : Error %s", e)
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'msg': "Error : " + str(e),
                    })
            else:
                status = "REJECTED"
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred",
                })


        else:
            status = "REJECTED"
            status_code = 500
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': "Params Not Available",
            })


class PurchaseOrderController(http.Controller):

    @http.route(['/purchase/order'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_purchase_order_create(self, **post):

        _logger.info("Service API : Data Received, Processing ......")

        status_code = 500
        status = "REJECTED"

        if not post:
            _logger.info("Service API : No Data Received or Incorrect Data Format!")
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': "No Data Received or Incorrect Data Format!",
            })

        _logger.info("Service API : Raw Data (JSON) Log Created")

        params = post.copy()

        _logger.info("Service API : Raw Data (JSON) copied")

        if params:
            if not params.get('username', False) \
                    or not params.get('password', False) \
                    :
                _logger.info("Service API : Login Parameters Not Available. Returning")
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "Missing Parameters",
                })

            user_id = request.env['res.users'].sudo().search([('login', '=', str(params['username']))],
                                                             limit=1)
            # user_id.update({'company_id':int(params['company_id'])})
            _logger.info("Service API : Company IDs of User (%s)  (%s)", user_id.name, user_id.company_ids)
            if not user_id:
                _logger.info('Service API : User Not Available Returning')
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred - User Not Available",
                })

            log_vals = {}

            if 'is_approved' in params:
                is_approved = (params.get('is_approved'))
                log_vals.update({'is_approved': is_approved or False})

            if 'purchase_req_id' in params:
                purchase_req_id = int(params.get('purchase_req_id'))
                log_vals.update({'request_id': purchase_req_id or False})

            if 'purchase_order_id' in params:
                purchase_order_id = int(params.get('purchase_order_id'))
                log_vals.update({'purchase_order_id': purchase_order_id or False})

            if 'event_type' in params:
                event_type = (params.get('event_type'))
                log_vals.update({'event_type': event_type or False})

            if 'order_deadline' in params:
                date_order = (params.get('order_deadline'))
                log_vals.update({'date_order': date_order or False})

            if 'receipt_date' in params:
                date_planned = (params.get('receipt_date'))
                log_vals.update({'date_planned': date_planned or False})

            if 'vendor_id' in params:
                partner_id = int(params.get('vendor_id', False))
                log_vals.update({'partner_id': partner_id or False})

            if 'warehouse_id' in params:
                warehouse_id = int(params.get('warehouse_id', False))
                log_vals.update({'warehouse_id': warehouse_id or False})

            if 'vendor_reference' in params:
                partner_ref = (params.get('vendor_reference', False))
                log_vals.update({'partner_ref': partner_ref or False})

            if 'purchase_mode' in params:
                hms_purchase_mode = (params.get('purchase_mode', False))
                log_vals.update({'hms_purchase_mode': hms_purchase_mode or False})

            if 'purchase_representative' in params:
                user_id = int(params.get('purchase_representative', False))
                log_vals.update({'user_id': user_id or False})

            if 'picking_type_id' in params:
                picking_type_id = int(params.get('picking_type_id', False))
                log_vals.update({'picking_type_id': picking_type_id or False})

            if 'incoterm' in params:
                incoterm_id = int(params.get('incoterm', False))
                log_vals.update({'incoterm_id': incoterm_id or False})

            if 'payment_terms' in params:
                payment_term_id = int(params.get('payment_terms', False))
                log_vals.update({'payment_term_id': payment_term_id or False})

            if 'fiscal_position' in params:
                fiscal_position_id = int(params.get('fiscal_position', False))
                log_vals.update({'fiscal_position_id': fiscal_position_id or False})

            if 'operating_unit_id' in params:
                operating_unit_id = int(params.get('operating_unit_id', False))
                log_vals.update({'operating_unit_id': operating_unit_id or False})

            if 'requesting_operating_unit_id' in params:
                requesting_operating_unit_id = int(params.get('requesting_operating_unit_id', False))
                log_vals.update({'requesting_operating_unit_id': requesting_operating_unit_id or False})

            if 'order_lines' in params:
                order_lines = params.get('order_lines', False)
                log_vals.update({'order_lines': order_lines or False})

            if 'company_id' in params:
                company_id = int(params.get('company_id', False))
                log_vals.update({'company_id': company_id or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'purchase.order.api.create',
                                                 'action_purchase_order_create', [log_vals])
                    purchase_order_dict = json.loads(response)
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': purchase_order_dict['status'],
                        'status_code': purchase_order_dict['status_code'],
                        'purchase_order_id': purchase_order_dict['purchase_order_id'],
                        'order_status': purchase_order_dict['order_status'],
                        'receipt_id': purchase_order_dict['receipt_id']

                    })

                except Exception as e:
                    status = "REJECTED"
                    status_code = 500
                    _logger.info("Service API : Error %s", e)
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'msg': "Error : " + str(e),
                    })
            else:
                status = "REJECTED"
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred",
                })


        else:
            status = "REJECTED"
            status_code = 500
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': "Params Not Available",
            })
