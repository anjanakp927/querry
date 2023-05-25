import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime


_logger = logging.getLogger(__name__)


class CoaCreateAPI(models.Model):
    _name = 'account.group.api.create'

    @api.model
    def action_create_account_group(self, values):

        account_group_id = self.env['account.group'].create(values)
        if account_group_id:
            _logger.info("Service API : Account Group Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'account_group_id': account_group_id.id

            })

