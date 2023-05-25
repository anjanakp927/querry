import xmlrpc
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class QMProduction(http.Controller):
    @http.route(['/qmproduction/'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_partner_create(self, **post):

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
            if 'qmproduction_id' in params:
                qmproduction_id = int(params.get('qmproduction_id'))
                log_vals.update({'qmproduction_id': qmproduction_id or False})

            if 'event_type' in params:
                event_type = params.get('event_type')
                log_vals.update({'event_type': event_type or False})

            if 'sl_no' in params:
                sl_no = int(params.get('sl_no'))
                log_vals.update({'sl_no': sl_no or False})

            if 'date' in params:
                date = params.get('date', False)
                log_vals.update({'date': date or False})

            if 'debit_head' in params:
                debit_head = params.get('debit_head')
                log_vals.update({'debit_head': debit_head or False})

            if 'from_stock' in params:
                from_stock = params.get('from_stock')
                log_vals.update({'from_stock': from_stock or False})

            if 'from_quarry' in params:
                from_quarry = params.get('from_quarry')
                log_vals.update({'from_quarry': from_quarry or False})

            if 'feeded_qty' in params:
                feeded_qty = params.get('feeded_qty')
                log_vals.update({'feeded_qty': feeded_qty or False})

            if 'to_stock' in params:
                to_stock = params.get('to_stock')
                log_vals.update({'to_stock': to_stock or False})

            if 'feeded_qty_purchse' in params:
                feeded_qty_purchse = params.get('feeded_qty_purchse')
                log_vals.update({'feeded_qty_purchse': feeded_qty_purchse or False})

            if 'to_stock_purchase' in params:
                to_stock_purchase = params.get('to_stock_purchase')
                log_vals.update({'to_stock_purchase': to_stock_purchase or False})


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

            if 'qmproduction_lines' in params:
                qmproduction_lines = params.get('qmproduction_lines', False)
                log_vals.update({'qmproduction_lines': qmproduction_lines or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'qm.production.api.create',
                                                 'action_create_qmproduction', [log_vals])
                    qmproduction_dict = json.loads(response)

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'qmproduction_id': qmproduction_dict['qmproduction_id'],

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
