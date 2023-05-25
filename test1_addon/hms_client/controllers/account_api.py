import xmlrpc
import logging
import json
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)


class AccountRequestController(http.Controller):

    @http.route(['/account/verify'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_account_verify(self, **post):
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

        _logger.info("Service API : Raw Data (JSON) Log Created (%s) (%s)",request.env.get('HTTP_X_FORWARDED_HOST', '').split(':')[0],request.env.cr.dbname)

        params = post.copy()

        _logger.info("Service API : Raw Data (JSON) copied")

        for i in params['values']:
            if not i.get('username', False) \
                    or not i.get('password', False) \
                    :
                _logger.info("Service API : Login Parameters Not Available. Returning")
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "Missing Parameters",
                })

            user_id = request.env['res.users'].sudo().search([('login', '=', str(i['username']))],
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

            if 'account_id' in i:
                account_id = i.get('account_id', False)
                log_vals.update({'account_id': account_id or False})

            if i['username'] and i['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(i['password']),
                                                 'coa.api.search',
                                                 'action_search_coa', [log_vals])
                    account_dict = json.loads(response)  # converted

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'partner_id': account_dict['account_id'],
                    })

                except Exception as e:
                    status = "REJECTED"
                    status_code = 500
                    _logger.info("Service API : Error (%s)",e)
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'msg': "An Error Occurred",
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

    @http.route(['/coa'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_coa_post(self, **post):

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

            if 'event_type' in params:
                event_type = params.get('event_type')
                log_vals.update({'event_type': event_type or False})

            if 'account_id' in params:
                account_id = int(params.get('account_id'))
                log_vals.update({'account_id': account_id or False})

            if 'code' in params:
                code = params.get('code', False)
                log_vals.update({'code': code or False})

            if 'name' in params:
                name = params.get('name', False)
                log_vals.update({'name': name or False})

            if 'user_type_id' in params:
                type = int(params.get('user_type_id', False))
                log_vals.update({'user_type_id': type or False})

            if 'tax_ids' in params:
                tax_ids = params.get('tax_ids', False)
                log_vals.update({'tax_ids': tax_ids or False})

            if 'allowed_journal_ids' in params:
                allowed_journal_ids = params.get('allowed_journal_ids', False)
                log_vals.update({'allowed_journal_ids': allowed_journal_ids or False})

            if 'group_id' in params:
                group_id = params.get('group_id', False)
                log_vals.update({'group_id': group_id or False})

            if 'reconcile' in params:
                reconcile = params.get('reconcile', False)
                log_vals.update({'reconcile': reconcile or False})

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
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']), 'coa.api.create',
                                           'action_create_coa', [log_vals])

                    account_dict = json.loads(response)
                    return json.dumps({
                        'status': account_dict['status'],
                        'status_code': account_dict['status_code'],
                        'account_id': account_dict['account_id'],
                      })
                except Exception as e:
                    status = "REJECTED"
                    status_code = 500
                    _logger.info("Service API : Error (%s)", e)
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
                    'msg': "Error : Required Parameters Not Available ",
                })


        else:
            status = "REJECTED"
            status_code = 500
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': "Params Not Available",
            })




