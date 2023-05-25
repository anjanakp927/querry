import xmlrpc
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WarehousesController(http.Controller):

    @http.route(['/warehouses/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_warehouses_create(self, **post):

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

            if 'warehouse' in params:
                warehouse = params.get('warehouse', False)
                log_vals.update({'name': warehouse or False})

            if 'short_name' in params:
                short_name = params.get('short_name', False)
                log_vals.update({'code': short_name or False})

            if 'partner_id' in params:
                partner_id = int(params.get('partner_id'))
                log_vals.update({'partner_id': partner_id or False})

            if 'purchase_journal' in params:
                purchase_journal = int(params.get('purchase_journal'))
                log_vals.update({'l10n_in_purchase_journal_id': purchase_journal or False})

            if 'sale_journal' in params:
                sale_journal = int(params.get('sale_journal'))
                log_vals.update({'l10n_in_sale_journal_id': sale_journal or False})

            if 'operating_unit_id' in params:
                operating_unit_id = int(params.get('operating_unit_id', False))
                log_vals.update({'operating_unit_id': operating_unit_id or False})

            # if 'operating_unit_ids' in params:
            #     operating_unit_ids = params.get('operating_unit_ids', False)
            #     log_vals.update({'operating_unit_ids': operating_unit_ids or False})

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
                                                 'warehouses.api.create',
                                                 'action_create_warehouses', [log_vals])
                    warehouses_dict = json.loads(response)  # converted

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'warehouse_id': warehouses_dict['warehouse_id'],
                        'location_id': warehouses_dict['location_id'],
                        'receipt_id': warehouses_dict['receipt_id'],
                        'delivery_id': warehouses_dict['delivery_id'],

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
