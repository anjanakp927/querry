import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime


_logger = logging.getLogger(__name__)


class OUCreateAPI(models.Model):
    _name = 'ou.api.create'

    @api.model
    def action_create_ou(self, values):



        ou_vals = {}

        company_obj = False

        if 'code' in values:
            code = values.get('code', False)
            ou_vals.update({'code': code or False})

        if 'name' in values:
            name = values.get('name', False)
            ou_vals.update({'name': name or False})


        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            ou_vals.update({'company_id': company_id or False})
            company_obj = self.env['res.company'].sudo().search([('id', '=', company_id)],
                                                             limit=1)
            if company_obj:
                ou_vals.update({'partner_id': company_obj.partner_id.id or False})

        operating_unit_id = self.env['operating.unit'].create(ou_vals)
        if operating_unit_id:
            _logger.info("Service API : Operating Unit Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'operating_unit_id': operating_unit_id.id,
            })
        else:
            status = 'REJECTED'
            status_code = 400
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg' : 'Error'
            })


