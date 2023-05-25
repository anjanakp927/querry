import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class JournalCreateAPI(models.Model):
    _name = 'journal.api.create'

    @api.model
    def action_create_journal(self, values):
        journal = self.env['account.journal'].create(values)
        if journal:
            _logger.info("Service API : Journal Created (%s) ", journal.id)
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'journal_id': journal.id,
            })

