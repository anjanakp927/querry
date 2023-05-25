from soupsieve.util import lower
from odoo import models
from odoo import http
import xmlrpc
import logging
import json
from odoo.http import request

_logger = logging.getLogger(__name__)


class AccountMoveController(http.Controller):

    @http.route(['/account/move/'], type='json', auth='public', methods=['POST'], csrf=False)
    def account_move_post(self, **post):

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

            if 'invoice_id' in params:
                invoice_id = int(params.get('invoice_id'))
                log_vals.update({'invoice_id': invoice_id or False})

            if 'payment_id' in params:
                payment_id = int(params.get('payment_id',False))
                log_vals.update({'payment_id': payment_id or False})

            if 'name' in params:
                name = params.get('name', False)
                log_vals.update({'name': name or False})

            if 'partner_no' in params:
                partner_id = int(params.get('partner_no', False))
                log_vals.update({'partner_id': partner_id or False})

            if 'move_type' in params:
                move_type = params.get('move_type', False)
                log_vals.update({'move_type': move_type or False})

            if 'payment_ref' in params:
                payment_ref = params.get('payment_ref', False)
                log_vals.update({'payment_reference': payment_ref or False})

            if 'reference' in params:
                ref = params.get('reference', False)
                log_vals.update({'ref': ref or False})

            if 'invoice_date' in params:
                invoice_date = params.get('invoice_date', False)
                log_vals.update({'invoice_date': invoice_date or False})

            if 'invoice_date_due' in params:
                invoice_date_due = params.get('invoice_date_due', False)
                log_vals.update({'invoice_date_due': invoice_date_due or False})

            if 'gst_treatment' in params:
                gst_treatment = params.get('gst_treatment', False)
                log_vals.update({'l10n_in_gst_treatment': gst_treatment or False})

            if 'journal_id' in params:
                journal_id = int(params.get('journal_id', False))
                log_vals.update({'journal_id': journal_id or False})

            if 'operating_unit_id' in params:
                operating_unit_id = int(params.get('operating_unit_id', False))
                log_vals.update({'operating_unit_id': operating_unit_id or False})

            if 'is_payment' in params:
                is_payment = params.get('is_payment', False)
                log_vals.update({'is_payment':lower(is_payment ) or False})

            if 'payment_journal_id' in params:
                payment_journal_id = int(params.get('payment_journal_id', False))
                log_vals.update({'payment_journal_id': payment_journal_id or False})

            if 'is_round_off' in params:
                is_round_off = params.get('is_round_off', False)
                log_vals.update({'is_round_off': lower(is_round_off) or False})

            if 'round_off_value' in params:
                round_off_value = params.get('round_off_value', False)
                log_vals.update({'round_off_value': round_off_value or False})

            if 'round_off_account_id' in params:
                round_off_account_id = int(params.get('round_off_account_id', False))
                log_vals.update({'round_off_account_id': round_off_account_id or False})

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

            if 'invoice_lines' in params:
                invoice_lines = params.get('invoice_lines', False)
                log_vals.update({'invoice_lines': invoice_lines or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'account.move.api.create',
                                                 'action_create_move', [log_vals])

                    account_move_dict = json.loads(response)
                    status = 'SUCCESS'
                    status_code = 200
                    if 'payment_id' in account_move_dict :
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'account_move_id': account_move_dict['account_move_id'],
                            'Payment_id': account_move_dict['payment_id']
                        })
                    else:
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'account_move_id': account_move_dict['account_move_id'],
                        })

                    # return str(id)
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
