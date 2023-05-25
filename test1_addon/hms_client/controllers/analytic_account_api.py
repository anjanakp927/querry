from odoo import http
import xmlrpc
import logging
import json
from odoo.http import request

_logger = logging.getLogger(__name__)


class AnalyticAccountController(http.Controller):

    @http.route(['/account/analytic_account/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_account_analytic_account_create(self, **post):
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

            if 'name' in params:
                name = params.get('name', False)
                log_vals.update({'name': name or False})
            if 'reference' in params:
                reference = params.get('reference', False)
                log_vals.update({'code': reference or False})
            if 'group_id' in params:
                group_id = int(params.get('group_id', False))
                log_vals.update({'group_id': group_id or False})
            if 'partner_id' in params:
                partner_id = int(params.get('partner_id', False))
                log_vals.update({'partner_id': partner_id or False})

            if 'operating_unit_ids' in params:
                operating_unit_ids = params.get('operating_unit_ids', False)
                log_vals.update({'operating_unit_ids': operating_unit_ids or False})

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
                                                 'analytic_account.api.create',
                                                 'action_create_analytic_account', [log_vals])

                    analytic_account_dict = json.loads(response)  # converted
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'analytic_account_id' : analytic_account_dict['analytic_account_id'],
                    })

                except Exception as e:
                    _logger.info("Service API : Error %s", e)
                    status = "REJECTED"
                    status_code = 500
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


    @http.route(['/account/analytic_account_group/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_account_analytic_account_group_create(self, **post):
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

            if 'name' in params:
                name = params.get('name', False)
                log_vals.update({'name': name or False})
            if 'parent_id' in params:
                parent_id = params.get('parent_id', False)
                log_vals.update({'parent_id': int(parent_id) or False})
            if 'description' in params:
                description = params.get('description', False)
                log_vals.update({'description': description or False})

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
                                                 'analytic_account.api.create',
                                                 'action_create_analytic_account_group', [log_vals])

                    analytic_account_dict = json.loads(response)  # converted
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'analytic_account_group' : analytic_account_dict['analytic_account_group_id'],
                    })

                except Exception as e:
                    _logger.info("Service API : Error %s", e)
                    status = "REJECTED"
                    status_code = 500
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
