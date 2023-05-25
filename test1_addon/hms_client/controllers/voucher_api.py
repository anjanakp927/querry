from odoo import http
import xmlrpc
import logging
import json
from odoo.http import request

_logger = logging.getLogger(__name__)


class VoucherController(http.Controller):

    @http.route(['/account/vouchers/'], type='json', auth='public', methods=['POST'], csrf=False)
    def accounting_voucher_post(self, **post):
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

            if 'name' in params:
                name = params.get('name', False)
                log_vals.update({'name': name or False})

            if 'voucher_id' in params:
                voucher_id = int(params.get('voucher_id'))
                log_vals.update({'voucher_id': voucher_id or False})

            if 'voucher_type' in params:
                voucher_type = params.get('voucher_type', False)
                log_vals.update({'voucher_type': voucher_type or False})

            # if 'voucher_no' in params:
            #     voucher_no = params.get('voucher_no', False)
            #     log_vals.update({'voucher_no': voucher_no or False})

            if 'voucher_date' in params:
                date = params.get('voucher_date', False)
                log_vals.update({'date': date or False})

            if 'received_from' in params:
                received_from = params.get('received_from', False)
                log_vals.update({'received_from': received_from or False})

            if 'paid_to' in params:
                paid_to = params.get('paid_to', False)
                log_vals.update({'paid_to': paid_to or False})

            if 'operating_unit_id' in params:
                operating_unit_id = params.get('operating_unit_id', False)
                log_vals.update({'operating_unit_id': operating_unit_id or False})

            if 'cheque_no' in params:
                cheque_no = params.get('cheque_no', False)
                log_vals.update({'cheque_no': cheque_no or False})

            if 'cheque_date' in params:
                cheque_date = params.get('cheque_date', False)
                log_vals.update({'cheque_date': cheque_date or False})

            if 'reference' in params:
                reference = params.get('reference', False)
                log_vals.update({'ref': reference or False})

            if 'voucher_update_id' in params:
                voucher_update_id = params.get('voucher_update_id', False)
                log_vals.update({'voucher_update_id': voucher_update_id or False})

            if 'journal_id' in params:
                journal_id = int(params.get('journal_id', False))
                log_vals.update({'journal_id': journal_id or False})

            if 'account_id' in params:
                account_id = int(params.get('account_id', False))
                log_vals.update({'account_id': account_id or False})

            if 'amount' in params:
                amount = params.get('amount', False)
                log_vals.update({'amount': amount or False})

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

            if 'line_ids' in params:
                line_ids = params.get('line_ids', False)
                log_vals.update({'line_ids': line_ids or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:
                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'voucher.api.create',
                                                 'action_create_voucher', [log_vals])
                    voucher_dict = json.loads(response)
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'voucher_id': voucher_dict['voucher_id'],
                    })

                except Exception as e:
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
