import xmlrpc
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class StockRequest(http.Controller):
    @http.route(['/stock_request/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_stock_req_create(self, **post):

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
            if not user_id:
                _logger.info('Service API : User Not Available Returning')
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred - User Not Available",
                })

            log_vals = {}

            if 'request_by' in params:
                request_by = int(params.get('request_by'))
                log_vals.update({'request_by': request_by or False})

            if 'date' in params:
                request_date = params.get('date')
                log_vals.update({'request_date': request_date or False})

            if 'request_lines' in params:
                request_lines = params.get('request_lines', False)
                log_vals.update({'request_lines': request_lines or False})

            if 'operating_unit_id' in params:
                operating_unit_id = int(params.get('operating_unit_id', False))
                log_vals.update({'operating_unit_id': operating_unit_id or False})

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
                                                 'stock_request.api.create',
                                                 'action_create_stock_request', [log_vals])
                    stock_request = json.loads(response)

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'stock_request_id': stock_request['stock_request_id']
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


class StockIssueIndentIssue(http.Controller):
    @http.route(['/stock_issue/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_stock_issue_create(self, **post):

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
            if not user_id:
                _logger.info('Service API : User Not Available Returning')
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred - User Not Available",
                })

            log_vals = {}

            if 'date' in params:
                request_date = params.get('date')
                log_vals.update({'request_date': request_date or False})

            if 'request_by' in params:
                request_by = int(params.get('request_by'))
                log_vals.update({'request_by': request_by or False})

            if 'issued_by' in params:
                issued_by = int(params.get('issued_by'))
                log_vals.update({'issued_by': issued_by or False})

            if 'stock_request_id' in params:
                stock_request_id = int(params.get('stock_request_id'))
                log_vals.update({'stock_request_id': stock_request_id or False})

            if 'warehouse_id' in params:
                warehouse_id = int(params.get('warehouse_id'))
                log_vals.update({'warehouse_id': warehouse_id or False})

            if 'stock_lines' in params:
                stock_lines = (params.get('stock_lines'))
                log_vals.update({'stock_lines': stock_lines or False})

            if 'operating_unit_id' in params:
                operating_unit_id = int(params.get('operating_unit_id'))
                log_vals.update({'operating_unit_id': operating_unit_id or False})

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
                                                 'stock_issue.api',
                                                 'action_create_stock_issue', [log_vals])
                    stock_issue = json.loads(response)

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'stock_issue_id': stock_issue['stock_issue_id'],
                        'stock_delivery_id': stock_issue['stock_delivery_id'],

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
