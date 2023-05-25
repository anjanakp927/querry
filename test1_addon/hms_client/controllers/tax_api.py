import xmlrpc
import logging
import json
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)


class TaxController(http.Controller):


    @http.route(['/account/tax/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_tax_post(self, **post):

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

            if 'type' in params:
                type = params.get('type', False)
                log_vals.update({'type_tax_use': type or False})

            if 'amount_type' in params:
                amount_type =  params.get('amount_type', False)
                log_vals.update({'amount_type': amount_type or False})
                
            if 'amount' in params:
                amount = float(params.get('amount', False))
                log_vals.update({'amount': amount or False})
                
            if 'label_on_invoice' in params:
                label_on_invoice = params.get('label_on_invoice', False)
                log_vals.update({'label_on_invoice': label_on_invoice or False})

            if 'tax_group' in params:
                tax_group = params.get('tax_group', False)
                log_vals.update({'tax_group': tax_group or False})

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


            if 'invoice_distribution' in params:
                invoice_distribution = params.get('invoice_distribution', False)
                log_vals.update({'invoice_distribution': invoice_distribution or False})

            if 'refund_distribution' in params:
                refund_distribution = params.get('refund_distribution', False)
                log_vals.update({'refund_distribution': refund_distribution or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']), 'tax.api.create',
                                           'action_create_tax', [log_vals])
                    tax_dict = json.loads(response)

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'tax_id': tax_dict['account_tax_id'],
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




