from odoo import http
import xmlrpc
import logging
import json
from odoo.http import request

_logger = logging.getLogger(__name__)


class JournalEntryController(http.Controller):

    @http.route(['/account/journal_entry/'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_account_journal_entry_create(self, **post):
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

            if 'journal_entry_id' in params:
                journal_entry_id = int(params.get('journal_entry_id'))
                log_vals.update({'journal_entry_id': journal_entry_id or False})

            if 'name' in params:
                name=params.get('name')
                log_vals.update({'name':name or False})

            if 'operating_unit_id' in params:
                operating_unit_id = int(params.get('operating_unit_id', False))
                log_vals.update({'operating_unit_id': operating_unit_id or False})


            if 'accounting_date' in params:
                accounting_date = params.get('accounting_date', False)
                log_vals.update({'accounting_date': accounting_date or False})

            if 'reference' in params:
                reference = params.get('reference', False)
                log_vals.update({'reference': reference or False})

            if 'journal_id' in params:
                journal_id = params.get('journal_id', False)
                log_vals.update({'journal_id': journal_id or False})

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


            if 'journal_lines' in params:
                journal_lines = params.get('journal_lines', False)
                log_vals.update({'journal_lines': journal_lines or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'journal.entry.api.create',
                                                 'action_create_journal_entry', [log_vals])

                    journal_entry_dict = json.loads(response)  # converted
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'journal_entry_id' : journal_entry_dict['journal_entry_id'],
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
