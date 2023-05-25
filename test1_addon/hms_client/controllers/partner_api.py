import xmlrpc
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PartnerRequestController(http.Controller):

    @http.route(['/partner/verify'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_partner_verify(self, **post):
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

            if 'partner_id' in i:
                partner_id = i.get('partner_id', False)
                log_vals.update({'partner_id': partner_id or False})

            if i['username'] and i['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(i['password']),
                                                 'partner.api.search',
                                                 'action_search_partner', [log_vals])
                    partner_dict = json.loads(response)  # converted

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'partner_id': partner_dict['partner_id'],
                    })

                except Exception as e:
                    status = "REJECTED"
                    status_code = 500
                    _logger.info("Service API : Error %s", e)
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

    @http.route(['/partner'], type='json', auth='public', methods=['POST'], csrf=False)
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

            if 'event_type' in params:
                event_type = params.get('event_type')
                log_vals.update({'event_type': event_type or False})

            if 'partner_id' in params:
                partner_id = int(params.get('partner_id'))
                log_vals.update({'partner_id': partner_id or False})

            if 'name' in params:
                name = params.get('name', False)
                log_vals.update({'name': name or False})

            if 'company_type' in params:
                type = params.get('company_type', False)
                log_vals.update({'company_type': type or False})

            if 'street' in params:
                street = params.get('street', False)
                log_vals.update({'street': street or False})

            if 'street2' in params:
                street2 = params.get('street2', False)
                log_vals.update({'street2': street2 or False})

            if 'city' in params:
                city = params.get('city', False)
                log_vals.update({'city': city or False})

            if 'state_id' in params:
                state = int(params.get('state_id', False))
                log_vals.update({'state_id': state or False})

            if 'zip' in params:
                zip = params.get('zip', False)
                log_vals.update({'zip': zip or False})

            if 'country_id' in params:
                country = int(params.get('country_id', False))
                log_vals.update({'country_id': country or False})

            if 'phone' in params:
                phone = params.get('phone', False)
                log_vals.update({'phone': phone or False})

            if 'mobile' in params:
                mobile = params.get('mobile', False)
                log_vals.update({'mobile': mobile or False})

            if 'email' in params:
                email = params.get('email', False)
                log_vals.update({'email': email or False})

            if 'website' in params:
                website = params.get('website', False)
                log_vals.update({'website': website or False})

            if 'gst_no' in params:
                vat = params.get('gst_no', False)
                log_vals.update({'vat': vat or False})

            if 'gst_treatment' in params:
                gst = params.get('l10n_in_gst_treatment', False)
                log_vals.update({'l10n_in_gst_treatment': gst or False})

            if 'account_receivable_id' in params:
                receivable_account = int(params.get('account_receivable_id', False))
                log_vals.update({'property_account_receivable_id': receivable_account or False})
            else:
                _logger.info('Service API : Account Receivable ID Not Available Returning')
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred -Account Receivable ID Not Available",
                })

            if 'account_payable_id' in params:
                payable_account = int(params.get('account_payable_id', False))
                log_vals.update({'property_account_payable_id': payable_account or False})
            else:
                _logger.info('Service API : Account Payable ID Not Available Returning')
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred -Account Payable ID Not Available",
                })

            if 'operating_unit_ids' in params:
                operating_unit_ids = params.get('operating_unit_ids', False)
                log_vals.update({'operating_unit_ids': operating_unit_ids or False})

            if 'bank_details' in params:
                bank_details = (params.get('bank_details', False))
                log_vals.update({'bank_details': bank_details or False})

            if 'company_ids' in params:
                company_ids = (params.get('company_ids', False))
                log_vals.update({'company_ids': company_ids or False})
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
                                                 'partner.api.create',
                                                 'action_create_partner', [log_vals])
                    partner_dict = json.loads(response)  # converted

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'partner_id': partner_dict['partner_id'],

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
