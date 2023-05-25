import xmlrpc
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class StockTransferController(http.Controller):

    @http.route(['/stock_transfer/create/'], type='json', auth='public', methods=['POST'], csrf=False)
    def stock_transfer_create(self, **post):

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

            if 'partner_id' in params:
                partner_id = int(params.get('partner_id'))
                log_vals.update({'partner_id': partner_id or False})

            if 'picking_type_id' in params:
                picking_type_id = int(params.get('picking_type_id'))
                log_vals.update({'picking_type_id': picking_type_id or False})

            if 'location_id' in params:
                location_id = int(params.get('location_id'))
                log_vals.update({'location_id': location_id or False})

            if 'location_dest_id' in params:
                location_dest_id = int(params.get('location_dest_id'))
                log_vals.update({'location_dest_id': location_dest_id or False})

            if 'scheduled_date' in params:
                scheduled_date = (params.get('scheduled_date'))
                log_vals.update({'scheduled_date': scheduled_date or False})

            if 'stock_lines' in params:
                stock_lines = (params.get('stock_lines'))
                log_vals.update({'stock_lines': stock_lines or False})

            if 'operating_unit_id' in params:
                operating_unit_id = params.get('operating_unit_id', False)
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
                                                 'stock_transfer.api.create',
                                                 'action_create_stock_transfer', [log_vals])
                    stock_transfer_dict = json.loads(response)  # converted

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': stock_transfer_dict['status'],
                        'status_code': stock_transfer_dict['status_code'],
                        'stock_transfer_id': stock_transfer_dict['stock_transfer_id'],
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
