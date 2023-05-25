import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class WarehousesCreateAPI(models.Model):
    _name = 'warehouses.api.create'

    @api.model
    def action_create_warehouses(self, vals):
        warehouse_vals = {}

        if 'partner_id' in vals:
            partner_id = int(vals.get('partner_id'))
            warehouse_vals.update({'partner_id': partner_id or False})

        if 'name' in vals:
            name = vals.get('name', False)
            warehouse_vals.update({'name': name or False})

        if 'code' in vals:
            code = vals.get('code', False)
            warehouse_vals.update({'code': code or False})

        if 'l10n_in_purchase_journal_id' in vals:
            l10n_in_purchase_journal_id = int(vals.get('l10n_in_purchase_journal_id'))
            warehouse_vals.update({'l10n_in_purchase_journal_id': l10n_in_purchase_journal_id or False})

        if 'l10n_in_sale_journal_id' in vals:
            l10n_in_sale_journal_id = int(vals.get('l10n_in_sale_journal_id'))
            warehouse_vals.update({'l10n_in_sale_journal_id': l10n_in_sale_journal_id or False})

        if 'operating_unit_id' in vals:
            operating_unit_id = int(vals.get('operating_unit_id'))
            warehouse_vals.update({'operating_unit_id': operating_unit_id or False})

        if 'company_id' in vals:
            company_id = int(vals.get('company_id', False))
            warehouse_vals.update({'company_id': company_id or False})
        else:
            _logger.info('Service API : Company ID Not Available Returning')
            status_code = 401
            return json.dumps({
                'status': 'REJECTED',
                'status_code': status_code,
                'msg': "An Error Occurred - Company ID Not Available",
            })

        warehouse_id = self.env['stock.warehouse'].create(warehouse_vals)
        if warehouse_id:
            _logger.info("Service API : Warehouse Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'warehouse_id': str(warehouse_id.id),
                'location_id': str(warehouse_id.lot_stock_id.id),
                'delivery_id': str(warehouse_id.out_type_id.id),
                'receipt_id': str(warehouse_id.in_type_id.id),

            })
