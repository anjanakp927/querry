import xmlrpc
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class SaleOrderController(http.Controller):

    @http.route(['/sale/order'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_sale_order_create(self, **post):

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

            if 'partner_id' in params:
                partner_id = (params.get('partner_id'))
                log_vals.update({'partner_id': partner_id or False})

            if 'sale_order_id' in params:
                sale_order_id = (params.get('sale_order_id'))
                log_vals.update({'sale_order_id': sale_order_id or False})

            if 'gst_treatment' in params:
                l10n_in_gst_treatment = (params.get('gst_treatment'))
                log_vals.update({'l10n_in_gst_treatment': l10n_in_gst_treatment or False})

            if 'event_type' in params:
                event_type = (params.get('event_type'))
                log_vals.update({'event_type': event_type or False})

            if 'expiration_date' in params:
                validity_date = (params.get('expiration_date'))
                log_vals.update({'validity_date': validity_date or False})

            if 'date_order' in params:
                date_order = (params.get('date_order'))
                log_vals.update({'date_order': date_order or False})

            if 'payment_terms' in params:
                payment_term_id = (params.get('payment_terms', False))
                log_vals.update({'payment_term_id': payment_term_id or False})

            if 'salesperson' in params:
                salesperson = (params.get('salesperson', False))
                log_vals.update({'salesperson': salesperson or False})

            if 'fiscal_position' in params:
                fiscal_position_id = (params.get('fiscal_position', False))
                log_vals.update({'fiscal_position_id': fiscal_position_id or False})

            if 'journal' in params:
                l10n_in_journal_id = (params.get('fiscal_position', False))
                log_vals.update({'l10n_in_journal_id': l10n_in_journal_id or False})

            if 'company_id' in params:
                company_id = (params.get('company_id', False))
                log_vals.update({'company_id': company_id or False})

            if 'operating_unit_id' in params:
                operating_unit_id = (params.get('operating_unit_id', False))
                log_vals.update({'operating_unit_id': operating_unit_id or False})

            if 'customer_reference' in params:
                client_order_ref = (params.get('customer_reference', False))
                log_vals.update({'client_order_ref': client_order_ref or False})

            if 'shipping_policy' in params:
                picking_policy = (params.get('shipping_policy', False))
                log_vals.update({'picking_policy': picking_policy or False})

            # if 'incoterm' in params:
            #     incoterm = (params.get('incoterm', False))
            #     log_vals.update({'incoterm': incoterm or False})

            if 'operating_unit_id' in params:
                operating_unit_id = (params.get('operating_unit_id', False))
                log_vals.update({'operating_unit_id': operating_unit_id or False})

            if 'warehouse_id' in params:
                warehouse_id = int(params.get('warehouse_id', False))
                log_vals.update({'warehouse_id': warehouse_id or False})

            if 'order_lines' in params:
                order_lines = params.get('order_lines', False)
                log_vals.update({'order_lines': order_lines or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'sale.order.api.create',
                                                 'action_sale_order_create', [log_vals])
                    sale_order_dict = json.loads(response)
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': sale_order_dict['status'],
                        'status_code': sale_order_dict['status_code'],
                        'sale_order_id': sale_order_dict['sale_order_id'],
                        'delivery_id': sale_order_dict['delivery_id']

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
