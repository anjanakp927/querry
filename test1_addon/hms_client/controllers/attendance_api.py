import xmlrpc
import logging
import json
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class AttendanceController(http.Controller):

    @http.route(['/attendance'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_coa_post(self, **post):
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

            if 'employee_code' in params:
                employee_code = (params.get('employee_code'))
                log_vals.update({'employee_code': employee_code or False})

            if 'check_in' in params:
                check_in = params.get('check_in', False)
                log_vals.update({'check_in': check_in or False})

            if 'check_out' in params:
                check_out = params.get('check_out', False)
                log_vals.update({'check_out': check_out or False})

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
                                                 'attendance.api.create',
                                                 'action_create_attendance', [log_vals])

                    attendance_dict = json.loads(response)

                    return json.dumps({
                        'status': attendance_dict['status'],
                        'status_code': attendance_dict['status_code'],
                        'attendance_id': attendance_dict['attendance_id'],
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