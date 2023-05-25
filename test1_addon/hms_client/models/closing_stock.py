import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class ClosingStockCreateAPI(models.Model):
    _name = 'closing_stock.api.create'

    @api.model
    def action_create_closing_stock(self, values):
        closing_stock_values = {}

        if 'closing_stock' in values:
            closing_stock = values.get('closing_stock')
            closing_stock_values.update({'closing_stock': closing_stock or False})

        if 'date' in values:
            closing_date = values.get('date', False)
            closing_stock_values.update({'closing_date': closing_date or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            closing_stock_values.update({'company_id': company_id or False})

        date_search = self.env['closing.stock.final.account'].search([("closing_date", "=", values.get('date'))])
        if date_search:
            date_search.update(closing_stock_values)
            _logger.info("Service API : Closing Stock Updated (%s)", date_search.id)
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'closing_stock_id': date_search.id,
                'dbname': self._cr.dbname,
            })
        else:
            closing_stock = self.env['closing.stock.final.account'].create(closing_stock_values)
            if closing_stock:
                _logger.info("Service API : Closing Stock Created (%s)", closing_stock.id)
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'closing_stock_id': closing_stock.id,
                    'dbname': self._cr.dbname,
                })
