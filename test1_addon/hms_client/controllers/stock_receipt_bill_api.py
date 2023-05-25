import xmlrpc
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class StockReceiptController(http.Controller):

    @http.route(['/stock_receipt/create/'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_receipt_create(self, **post):

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

            if 'create_bill' in params:
                create_bill = (params.get('create_bill'))
                log_vals.update({'create_bill': create_bill or False})

            if 'stock_lines' in params:
                stock_lines = (params.get('stock_lines'))
                log_vals.update({'stock_lines': stock_lines or False})

            if 'invoice_id' in params:
                invoice_id = int(params.get('invoice_id'))
                log_vals.update({'invoice_id': invoice_id or False})

            if 'receipt_id' in params:
                receipt_id = int(params.get('receipt_id'))
                log_vals.update({'receipt_id': receipt_id or False})

            # if 'warehouse_id' in params:
            #     warehouse_id = int(params.get('warehouse_id'))
            #     log_vals.update({'warehouse_id': warehouse_id or False})

            # if 'operating_unit_id' in params:
            #     operating_unit_id = params.get('operating_unit_id', False)
            #     log_vals.update({'operating_unit_id': operating_unit_id or False})

            if 'company_id' in params:
                company_id = int(params.get('company_id', False))
                log_vals.update({'company_id': company_id or False})
            else:
                _logger.info('Service API : Company ID Not Available Returning')
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred - Company ID Not Available",
                })

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'receipt.api.create',
                                                 'action_create_receipt', [log_vals])
                    receipt_dict = json.loads(response)  # converted

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': receipt_dict['status'],
                        'status_code': receipt_dict['status_code'],
                        'msg': receipt_dict['msg'],
                        'receipt_id': receipt_dict['picking_id'],
                        'back_order_id': receipt_dict['back_order'],
                        'purchase_order_id': receipt_dict['purchase_order_id'],
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
