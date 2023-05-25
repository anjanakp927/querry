import xmlrpc
import logging
import json
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MultiAccountRequestController(http.Controller):
    @http.route(['/coa_multicompany'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_mul_coa_post(self, **post):

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
                log_vals.update({'account_name': name or False})

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
                company_id = (params.get('company_id', False))
                log_vals.update({'company_id': company_id or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'mul_coa.api.create',
                                                 'action_create_mul_coa', [log_vals])

                    account_dict = json.loads(response)
                    return json.dumps({
                        'status': account_dict['status'],
                        'status_code': account_dict['status_code'],
                        'multi_company_id': account_dict['multi_company_id'],
                        'acc_data': account_dict['acc_data'],
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
