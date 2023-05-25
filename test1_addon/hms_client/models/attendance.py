import json
import logging
import pytz
import datetime
from decimal import Decimal

from odoo.http import request

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class AttendanceCreateAPI(models.Model):
    _name = 'attendance.api.create'

    @api.model
    def action_create_attendance(self, values):

        attendance_vals = {}
        check_in = False
        check_out = False
        attendence_id = False
        attendance = False
        if 'employee_code' in values:
            employee_code = values.get('employee_code')
            emp_rec = self.env['hr.employee'].search([('barcode', '=', employee_code)], limit=1)
            attendance_vals.update({'employee_id': emp_rec.id or False})

        if 'check_in' in values:
            check_in = values.get('check_in', False)
            fmt = '%Y-%m-%d %H:%M:%S'
            check_in = datetime.strptime(check_in, fmt)
            local = pytz.timezone(self.env.user.tz or pytz.utc)
            local_dt_from = local.localize(check_in, is_dst=None)
            utc_dt_from = local_dt_from.astimezone(pytz.utc)
            local_date_time_in = utc_dt_from.strftime('%Y-%m-%d %H:%M:%S')
            check_in = datetime.strptime(local_date_time_in, fmt)
            if check_in:
                attendance_vals.update({'check_in': check_in or False})
            else:
                status = 'REJECTED'
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': 'Wrong Date Format',
                })

        if 'check_out' in values:

            check_out = values.get('check_out', False)
            fmt = '%Y-%m-%d %H:%M:%S'
            check_out = datetime.strptime(check_out, fmt)
            local = pytz.timezone(self.env.user.tz or pytz.utc)
            local_dt_from = local.localize(check_out, is_dst=None)
            utc_dt_from = local_dt_from.astimezone(pytz.utc)
            local_date_time_out = utc_dt_from.strftime('%Y-%m-%d %H:%M:%S')
            check_out = datetime.strptime(local_date_time_out, fmt)

            if check_out:
                attendance_vals.update({'check_out': check_out or False})
            else:
                status = 'REJECTED'
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': 'Wrong Date Format',
                })

        employee_id = attendance_vals['employee_id']
        attendance_obj = self.env['hr.attendance']

        attendance_ob = attendance_obj.search([('employee_id', '=', employee_id)]).filtered(
            lambda attendance: attendance.check_in.date() == check_in.date())

        if attendance_ob and attendance_vals['check_in'] and 'check_out' in values:
            for rec in attendance_ob:
                attendence_id = self.env['hr.attendance'].search([('id', '=', rec.id)])
                if attendence_id:
                    attendence_id.update(
                        {'check_out': attendance_vals['check_out']})
                    attendance = attendence_id

        elif attendance_ob and attendance_vals['check_in'] and 'check_out' not in values:
            for rec in attendance_ob:
                attendence_id = self.env['hr.attendance'].search([('id', '=', rec.id)])

            _logger.info("Service API : Attendance Already Created")
            status = 'SUCCESS'
            status_code = 200
            msg = 'Attendance Already created.'
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'message': msg,
                'attendance_id': attendence_id.id,

            })

        else:
            attendance_id = self.env['hr.attendance'].create(attendance_vals)
            attendance = attendance_id

        if attendance:
            _logger.info("Service API : Attendance Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'attendance_id': attendance.id,
            })

        else:
            status = 'REJECTED'
            status_code = 400
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': 'Employee ID Not Available for Update',
            })


