import xmlrpc
import logging
import json
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ProductRequestController(http.Controller):

    @http.route(['/product/verify'], type='json', auth='public', methods=['POST'], csrf=False)
    def product_verify(self, **post):
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

        for i in params['values']:
            if not i.get('username', False) \
                    or not i.get('password', False) \
                    :
                _logger.info("Service API : Login Parameters Not Available. Returning")
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "Missing Parameters",
                })

            user_id = request.env['res.users'].sudo().search([('login', '=', str(i['username']))],
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

            if 'product_id' in i:
                product_id = i.get('product_id', False)
                log_vals.update({'product_id': product_id or False})

            if i['username'] and i['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(i['password']),
                                                 'product.api.search',
                                                 'action_search_product', [log_vals])
                    product_dict = json.loads(response)  # converted

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'product_id': product_dict['product_id'],
                    })

                except Exception as e:
                    status = "REJECTED"
                    status_code = 500
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'msg': "An Error Occurred",
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

    @http.route(['/product/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_product_post(self, **post):

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

        # coa_rawlog = request.env['coa.api.rawlog'].sudo().create({
        #     'data': post and str(post),
        # })

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
                log_vals.update({'type': type or False})

            if 'sale_ok' in params:
                sale_ok = params.get('sale_ok', False)
                log_vals.update({'sale_ok': sale_ok or False})

            if 'categ_id' in params:
                categ_id = int(params.get('categ_id', False))
                log_vals.update({'categ_id': categ_id or False})

            if 'list_price' in params:
                list_price = float(params.get('list_price', False))
                log_vals.update({'list_price': list_price or False})

            if 'uom_id' in params:
                uom_id = int(params.get('uom_id', False))
                log_vals.update({'uom_id': uom_id or False})

            if 'uom_po_id' in params:
                uom_po_id = int(params.get('uom_po_id', False))
                log_vals.update({'uom_po_id': uom_po_id or False})

            if 'default_code' in params:
                default_code = params.get('default_code', False)
                log_vals.update({'default_code': default_code or False})

            if 'barcode' in params:
                barcode = params.get('barcode', False)
                log_vals.update({'barcode': barcode or False})

            if 'hsn_code' in params:
                hsn_code = params.get('hsn_code', False)
                log_vals.update({'l10n_in_hsn_code_master': hsn_code or False})

            if 'taxes_id' in params:
                taxes_id = params.get('taxes_id', False)
                log_vals.update({'taxes_id': taxes_id or False})

            if 'account_income_id' in params:
                income_account = int(params.get('account_income_id', False))
                log_vals.update({'property_account_income_id': income_account or False})

            if 'account_expense_id' in params:
                expense_account = int(params.get('account_expense_id', False))
                log_vals.update({'property_account_expense_id': expense_account or False})

            if 'standard_price' in params:
                standard_price = float(params.get('standard_price', False))
                log_vals.update({'standard_price': standard_price or False})

            if 'description' in params:
                description = params.get('description', False)
                log_vals.update({'description': description or False})

            if 'operating_unit_ids' in params:
                operating_unit_ids = params.get('operating_unit_ids', False)
                log_vals.update({'operating_unit_ids': operating_unit_ids or False})

            if 'item_code' in params:
                item_code = params.get('item_code', False)
                log_vals.update({'item_code': item_code or False})
                
            if 'product_code' in params:
                product_code = params.get('product_code', False)
                log_vals.update({'product_code': product_code or False})

            if 'company_ids' in params:
                company_ids = (params.get('company_ids', False))
                log_vals.update({'company_ids': company_ids or False})
            # else:
            #     _logger.info('Service API : Company ID Not Available Returning')
            #     status_code = 401
            #     return json.dumps({
            #         'status': status,
            #         'status_code': status_code,
            #         'msg': "An Error Occurred - Company ID Not Available",
            #     })

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                _logger.info("Service API : Attempting to Create Product From Controller")
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url, allow_none=True))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'product.api.create',
                                                 'action_create_product', [log_vals])

                    product_dict = json.loads(response)  # converted

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'product_id': product_dict['product_id'],
                    })

                    # return str(id)
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
