from soupsieve.util import lower

from odoo import models
from odoo import http
import xmlrpc
import logging
import json
from odoo.http import request

_logger = logging.getLogger(__name__)


class AccountPaymentController(http.Controller):

    @http.route(['/account/payment/create/'], type='json', auth='public', methods=['POST'], csrf=False)
    def account_payment_post(self, **post):

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

            if 'payment_id' in params:
                payment_id = params.get('payment_id', False)
                log_vals.update({'payment_id': payment_id or False})

            if 'payment_type' in params:
                payment_type = params.get('payment_type', False)
                log_vals.update({'payment_type': payment_type or False})

            if 'name' in params:
                name=params.get('name',False)
                log_vals.update(({'name':name or False}))

            if 'payment_reference' in params:
                payment_reference = params.get('payment_reference', False)
                log_vals.update(({'payment_reference': payment_reference or False}))

            if 'partner_type' in params:
                partner_type = params.get('partner_type', False)
                log_vals.update({'partner_type': partner_type or False})

            if 'partner_id' in params:
                partner_id = params.get('partner_id', False)
                log_vals.update({'partner_id': partner_id or False})

            if 'destination_account' in params:
                destination_account = int(params.get('destination_account', False))
                log_vals.update({'destination_account': destination_account or False})

            if 'amount' in params:
                amount = params.get('amount', False)
                log_vals.update({'amount': amount or False})

            if 'date' in params:
                date = params.get('date', False)
                log_vals.update({'date': date or False})

            if 'journal_id' in params:
                journal_id = params.get('journal_id', False)
                log_vals.update({'journal_id': journal_id or False})

            if 'is_internal_transfer' in params:
                is_internal_transfer = params.get('is_internal_transfer', False)
                log_vals.update({'is_internal_transfer': lower(is_internal_transfer) or False})

            if 'destination_journal_id' in params:
                destination_journal_id = params.get('destination_journal_id', False)
                log_vals.update({'destination_journal_id': destination_journal_id or False})

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
                                                 'account.payment.api.create',
                                                 'action_create_payment', [log_vals])
                    account_move_dict = json.loads(response)

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'Payment id': account_move_dict['payment_id']
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
