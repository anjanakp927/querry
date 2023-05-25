import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class AnalyticAccountCreateAPI(models.Model):
    _name = 'analytic_account.api.create'

    @api.model
    def action_create_analytic_account(self, values):

        if 'operating_unit_ids' in values:
            operating_unit_ids = []
            operating_unit_string = values['operating_unit_ids']
            _logger.info("Service API : operating_unit_ids %s", operating_unit_string)
            if operating_unit_string:
                operating_unit_list = operating_unit_string.split(',')
                for operating_unit_id in operating_unit_list:
                    operating_unit_ids.append(int(operating_unit_id))
                _logger.info("Service API : operating_unit_ids Id List %s", operating_unit_ids)
                values.update({'operating_unit_ids': [(6, 0, operating_unit_ids or [])]})


        analytic_account = self.env['account.analytic.account'].create(values)

        if analytic_account:
            _logger.info("Service API : Analytic Account Created (%s) ",analytic_account.id)
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'analytic_account_id': analytic_account.id,
            })

    @api.model
    def action_create_analytic_account_group(self, values):

        analytic_account_group = self.env['account.analytic.group'].create(values)

        if analytic_account_group:
            _logger.info("Service API : Analytic Account Group Created (%s) ",analytic_account_group.id)
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'analytic_account_group_id': analytic_account_group.id,
            })
