import xmlrpc
from soupsieve.util import lower
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class InvoiceBillController(http.Controller):

    @http.route(['/invoice_bill'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_invoice_bill_create(self, **post):

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

            if 'mode' in params:
                mode = (params.get('mode', False))
                log_vals.update({'mode': mode or False})

            if 'event_type' in params:
                event_type = (params.get('event_type', False))
                log_vals.update({'event_type': event_type or False})

            if 'purchase_order_id' in params:
                purchase_order_id = (params.get('purchase_order_id', False))
                log_vals.update({'purchase_order_id': purchase_order_id or False})

            if 'sale_order_id' in params:
                sale_order_id = (params.get('sale_order_id', False))
                log_vals.update({'sale_order_id': sale_order_id or False})

            if 'company_id' in params:
                company_id = (params.get('company_id', False))
                log_vals.update({'company_id': company_id or False})

            if 'operating_unit_id' in params:
                operating_unit_id = (params.get('operating_unit_id', False))
                log_vals.update({'operating_unit_id': operating_unit_id or False})

            if 'accounting_date' in params:
                accounting_date = (params.get('accounting_date', False))
                log_vals.update({'accounting_date': accounting_date or False})

            if 'invoice_date' in params:
                invoice_date = (params.get('invoice_date', False))
                log_vals.update({'invoice_date': invoice_date or False})

            if 'invoice_date_due' in params:
                invoice_date_due = params.get('invoice_date_due', False)
                log_vals.update({'invoice_date_due': invoice_date_due or False})

            if 'gst_treatment' in params:
                gst_treatment = (params.get('gst_treatment', False))
                log_vals.update({'gst_treatment': gst_treatment or False})

            if 'is_round_off' in params:
                is_round_off = params.get('is_round_off', False)
                log_vals.update({'is_round_off': lower(is_round_off) or False})

            if 'round_off_value' in params:
                round_off_value = params.get('round_off_value', False)
                log_vals.update({'round_off_value': round_off_value or False})

            if 'round_off_account_id' in params:
                round_off_account_id = int(params.get('round_off_account_id', False))
                log_vals.update({'round_off_account_id': round_off_account_id or False})

            if 'order_lines' in params:
                order_lines = params.get('order_lines', False)
                log_vals.update({'order_lines': order_lines or False})

            if 'order_lines' in params:
                order_lines = params.get('order_lines', False)
                log_vals.update({'order_lines': order_lines or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'invoice.bill.api.create',
                                                 'action_invoice_bill_create', [log_vals])
                    invoice_bill_dict = json.loads(response)
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': invoice_bill_dict['status'],
                        'status_code': invoice_bill_dict['status_code'],
                        'sale_order_id': invoice_bill_dict['sale_order_id'],
                        'purchase_order_id': invoice_bill_dict['purchase_order_id'],
                        'bill_id': invoice_bill_dict['bill'],
                        'invoice_id': invoice_bill_dict['invoice'],

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
