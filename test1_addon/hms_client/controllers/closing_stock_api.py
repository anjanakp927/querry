import xmlrpc
import logging
import json
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ClosingStockController(http.Controller):

    @http.route(['/closing_stock/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_closings_stock(self, **post):

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

            if 'date' in params:
                date = params.get('date')
                log_vals.update({'date': date or False})

            if 'company_id' in params:
                company_id = int(params.get('company_id'))
                log_vals.update({'company_id': company_id or False})

            if 'closing_stock' in params:
                closing_stock = (params.get('closing_stock'))
                log_vals.update({'closing_stock': closing_stock or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'closing_stock.api.create',
                                                 'action_create_closing_stock', [log_vals])

                    closing_stock_dict = json.loads(response)
                    return json.dumps({
                        'status': closing_stock_dict['status'],
                        'status_code': closing_stock_dict['status_code'],
                        'closing_stock_id': closing_stock_dict['closing_stock_id'],
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


class QuarryDrillingRequestController(http.Controller):

    @http.route(['/drilling/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_drilling_post(self, **post):

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
                name = params.get('name')
                log_vals.update({'name': name or False})

            if 'quarry' in params:
                quarry = params.get('quarry')
                log_vals.update({'quarry': quarry or False})

            if 'date' in params:
                date = params.get('date')
                log_vals.update({'date': date or False})

            if 'type_of_drilling' in params:
                type_of_drilling = params.get('type_of_drilling')
                log_vals.update({'type_of_drilling': type_of_drilling or False})

            if 'compressor' in params:
                compressor = params.get('compressor')
                log_vals.update({'compressor': compressor or False})

            if 'jack_hammer_id' in params:
                jack_hammer_id = int(params.get('jack_hammer_id'))
                log_vals.update({'jack_hammer_id': jack_hammer_id or False})

            if 'drill_bit' in params:
                drill_bit = params.get('drill_bit')
                log_vals.update({'drill_bit': drill_bit or False})

            if 'jack_hammer_working' in params:
                jack_hammer_working = params.get('jack_hammer_working')
                log_vals.update({'jack_hammer_working': jack_hammer_working or False})

            if 'hole_sizes' in params:
                hole_sizes = params.get('hole_sizes')
                log_vals.update({'hole_sizes': hole_sizes or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'drilling.api.create',
                                                 'action_create_drilling', [log_vals])

                    quarry_dict = json.loads(response)
                    return json.dumps({
                        'status': quarry_dict['status'],
                        'status_code': quarry_dict['status_code'],
                        'drilling_id': quarry_dict['drilling_id'],
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


class QuarryRequestController(http.Controller):

    @http.route(['/quarry/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_quarry_post(self, **post):

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

            if 'quarry_name' in params:
                quarry_name = params.get('quarry_name')
                log_vals.update({'quarry_name': quarry_name or False})

            if 'area' in params:
                area = params.get('area')
                log_vals.update({'area': area or False})

            if 'village' in params:
                village = params.get('village', False)
                log_vals.update({'village': village or False})

            if 'taluk' in params:
                taluk = params.get('taluk', False)
                log_vals.update({'taluk': taluk or False})

            if 'district' in params:
                district = params.get('district', False)
                log_vals.update({'district': district or False})

            if 'state_id' in params:
                state_id = int(params.get('state_id', False))
                log_vals.update({'state_id': state_id or False})

            if 'estimated_output' in params:
                estimated_output = params.get('estimated_output', False)
                log_vals.update({'estimated_output': estimated_output or False})

            if 'distance_from_plant' in params:
                distance_from_plant = params.get('distance_from_plant', False)
                log_vals.update({'distance_from_plant': distance_from_plant or False})

            if 'run_time_to_plant' in params:
                run_time_to_plant = params.get('run_time_to_plant', False)
                log_vals.update({'run_time_to_plant': run_time_to_plant or False})

            if 'rent' in params:
                rent = params.get('rent', False)
                log_vals.update({'rent': rent or False})

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
                                                 'quarry.api.create',
                                                 'action_create_quarry', [log_vals])

                    quarry_dict = json.loads(response)
                    return json.dumps({
                        'status': quarry_dict['status'],
                        'status_code': quarry_dict['status_code'],
                        'quarry_id': quarry_dict['quarry_id'],
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


class MiningRequestController(http.Controller):

    @http.route(['/mining/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_mining_post(self, **post):

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
                name = params.get('name')
                log_vals.update({'name': name or False})

            if 'belongs_to' in params:
                belongs_to = params.get('belongs_to')
                log_vals.update({'belongs_to': belongs_to or False})

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
                                                 'mining.api.create',
                                                 'action_create_mining', [log_vals])

                    quarry_dict = json.loads(response)
                    return json.dumps({
                        'status': quarry_dict['status'],
                        'status_code': quarry_dict['status_code'],
                        'mining_id': quarry_dict['mining_id'],
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


class JackhammerRequestController(http.Controller):

    @http.route(['/mining/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_jackhammer_post(self, **post):

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

            if 'jack_hammer' in params:
                jack_hammer = params.get('jack_hammer')
                log_vals.update({'jack_hammer': jack_hammer or False})

            if 'asset_id' in params:
                asset_id = params.get('asset_id')
                log_vals.update({'asset_id': asset_id or False})

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
                                                 'jackhammer.api.create',
                                                 'action_create_jackhammer', [log_vals])

                    quarry_dict = json.loads(response)
                    return json.dumps({
                        'status': quarry_dict['status'],
                        'status_code': quarry_dict['status_code'],
                        'jackhammer_id': quarry_dict['jackhammer_id'],
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


class ExplosiveConsumptionMarkingRequestController(http.Controller):

    @http.route(['/explosiveconsumptionmarking/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_explosive_consumption_marking_post(self, **post):

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

            if 'blaster' in params:
                blaster = params.get('blaster')
                log_vals.update({'blaster': blaster or False})

            if 'date' in params:
                date = params.get('date')
                log_vals.update({'date': date or False})

            if 'material_items' in params:
                material_items = params.get('material_items')
                log_vals.update({'material_items': material_items or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'explosive_consumption_marking.api.create',
                                                 'action_create_explosive_consumption', [log_vals])

                    quarry_dict = json.loads(response)
                    return json.dumps({
                        'status': quarry_dict['status'],
                        'status_code': quarry_dict['status_code'],
                        'explosive_consumption_id': quarry_dict['explosive_consumption_id'],
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


class EfillingRequestController(http.Controller):

    @http.route(['/efilling/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_efilling_post(self, **post):

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

            if 'date' in params:
                date = params.get('date')
                log_vals.update({'date': date or False})

            if 'time' in params:
                time = params.get('time')
                log_vals.update({'time': time or False})

            if 'employee_id' in params:
                employee_id = int(params.get('employee_id'))
                log_vals.update({'employee_id': employee_id or False})

            if 'remarks' in params:
                remarks = params.get('remarks')
                log_vals.update({'remarks': remarks or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'e_filling.api.create',
                                                 'action_create_e_filling', [log_vals])

                    quarry_dict = json.loads(response)
                    return json.dumps({
                        'status': quarry_dict['status'],
                        'status_code': quarry_dict['status_code'],
                        'e_filling_id': quarry_dict['e_filling_id'],
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


class QuarryBlastingRequestController(http.Controller):

    @http.route(['/blasting/create'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_blasting_post(self, **post):

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

            if 'date' in params:
                date = params.get('date')
                log_vals.update({'date': date or False})

            if 'name' in params:
                name = params.get('name')
                log_vals.update({'name': name or False})

            if 'quarry' in params:
                quarry = int(params.get('quarry'))
                log_vals.update({'quarry': quarry or False})

            if 'type_of_blasting' in params:
                type_of_blasting = params.get('type_of_blasting')
                log_vals.update({'type_of_blasting': type_of_blasting or False})

            if 'labour_details' in params:
                labour_details = params.get('labour_details')
                log_vals.update({'labour_details': labour_details or False})

            if 'drill_hole_details' in params:
                drill_hole_details = params.get('drill_hole_details')
                log_vals.update({'drill_hole_details': drill_hole_details or False})

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'blasting.api.create',
                                                 'action_create_blasting', [log_vals])

                    quarry_dict = json.loads(response)
                    return json.dumps({
                        'status': quarry_dict['status'],
                        'status_code': quarry_dict['status_code'],
                        'blasting_id': quarry_dict['blasting_id'],
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
