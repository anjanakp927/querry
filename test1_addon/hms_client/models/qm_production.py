import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class QMProductionCreateAPI(models.Model):
    _name = 'qm.production.api.create'

    @api.model
    def action_create_qmproduction(self, values):
        qm_production_values = {}

        event_type = ''
        qmproduction_id = 0

        if qmproduction_id in values:
            qmproduction_id = int(values.get('qmproduction_id'))

        if 'event_type' in values:
            event_type = values.get('event_type')

        if 'sl_no' in values:
            sl_no = int(values.get('sl_no', False))
            qm_production_values.update({'sl_no': sl_no or False})

        if 'date' in values:
            date = values.get('date', False)
            qm_production_values.update({'date': date or False})

        if 'debit_head' in values:
            debit_head = values.get('debit_head', False)
            qm_production_values.update({'debit_head': debit_head or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            qm_production_values.update({'company_id': company_id or False})

        if 'from_stock' in values:
            from_stock = float(values.get('from_stock', False))
            qm_production_values.update({'from_stock': from_stock or False})

        if 'from_quarry' in values:
            from_quarry = float(values.get('from_quarry', False))

            qm_production_values.update({'from_quarry': from_quarry or False})

        if 'feeded_qty' in values:
            feeded_qty = float(values.get('feeded_qty', False))
            qm_production_values.update({'feeded_qty': feeded_qty or False})

        if 'to_stock' in values:
            to_stock = float(values.get('to_stock', False))
            qm_production_values.update({'to_stock': to_stock or False})

        if 'feeded_qty_purchse' in values:
            feeded_qty_purchse = float(values.get('feeded_qty_purchse', False))
            qm_production_values.update({'feeded_qty_purchse': feeded_qty_purchse or False})

        if 'to_stock_purchase' in values:
            to_stock_purchase = float(values.get('to_stock_purchase', False))
            qm_production_values.update({'to_stock_purchase': to_stock_purchase or False})


        if 'qmproduction_lines' in values:
            qmproduction = {}
            qmproduction_lines = values.get('qmproduction_lines')
            _logger.info("Service API : Invoice Details (%s)", qmproduction)
            qmproduction_pos = 0
            qmproduction_line_det = []
            for qmproduction_item in qmproduction_lines:
                qmproduction_line_items = {}

                _logger.info("Service API : Invoice Details (%s)", qmproduction_item)

                if 'quarry_name' in qmproduction_item:
                    qmproduction_line_items.update({'quarry_name': (qmproduction_item['quarry_name'])})
                if 'operation_mode' in qmproduction_item:
                    qmproduction_line_items.update({'operation_mode': (qmproduction_item['operation_mode'])})
                if 'contractor_id' in qmproduction_item:
                    qmproduction_line_items.update({'contractor_id': int(qmproduction_item['contractor_id'])})
                if 'loads' in qmproduction_item:
                    qmproduction_line_items.update({'loads': float(qmproduction_item['loads'])})
                if 'rate_loads' in qmproduction_item:
                    qmproduction_line_items.update({'rate_loads': float(qmproduction_item['rate_loads'])})
                if 'feeded_quantity' in qmproduction_item:
                    qmproduction_line_items.update({'feeded_quantity': float(qmproduction_item['feeded_quantity'])})
                if 'loading_mode' in qmproduction_item:
                    qmproduction_line_items.update({'loading_mode': (qmproduction_item['loading_mode'])})
                if 'loaded_by_id' in qmproduction_item:
                    qmproduction_line_items.update({'loaded_by_id': int(qmproduction_item['loaded_by_id'])})
                if 'vehicle_id' in qmproduction_item:
                    qmproduction_line_items.update({'vehicle_id': int(qmproduction_item['vehicle_id'])})
                if 'vehicle_account_id' in qmproduction_item:
                    qmproduction_line_items.update({'vehicle_account_id': int(qmproduction_item['vehicle_account_id'])})
                if 'driver_id' in qmproduction_item:
                    qmproduction_line_items.update({'driver_id': int(qmproduction_item['driver_id'])})
                if 'cleaner_id' in qmproduction_item:
                    qmproduction_line_items.update({'cleaner_id': int(qmproduction_item['cleaner_id'])})
                if 'load_rent' in qmproduction_item:
                    qmproduction_line_items.update({'load_rent': float(qmproduction_item['load_rent'])})
                if 'amount' in qmproduction_item:
                    qmproduction_line_items.update({'amount': float(qmproduction_item['amount'])})
                if 'effective_load' in qmproduction_item:
                    qmproduction_line_items.update({'effective_load': float(qmproduction_item['effective_load'])})
                if 'feeded_load' in qmproduction_item:
                    qmproduction_line_items.update({'feeded_load': float(qmproduction_item['feeded_load'])})

                qmproduction_line_det.append((0, qmproduction_pos, qmproduction_line_items))
                qmproduction_pos = qmproduction_pos + 1
            _logger.info("Service API : Invoice Lines Details (%s)", qmproduction_line_det)
            qm_production_values.update({'loading_ids': qmproduction_line_det})

        qmproduction_id = False
        action = False

        if event_type == 'create':
            qmproduction_id = self.env['qm.loading'].create(qm_production_values)

            if qmproduction_id:
                _logger.info("Service API : QM Production Created (%s)", qmproduction_id.id)
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'qmproduction_id': qmproduction_id.id,
                    'dbname': self._cr.dbname,
                })


        elif event_type == 'update':
            qmproduction_id = self.env['qm.loading'].search([('id', '=', values.get('qmproduction_id'))])
            qmproduction_line_ids = self.env['qm.loading.lines'].search([('loading_id', '=', qmproduction_id.id)])
            _logger.info("Service API : QM Production Remove >>>> (%s )", qmproduction_line_ids)


            if qmproduction_line_ids:
                qmproduction_line_ids.unlink()
                _logger.info("Service API : QM Production Remove <<<< (%s )", qmproduction_line_ids)

            if qmproduction_id:
                _logger.info("Service API : QM Production Starting Update (%s)", qmproduction_id.id)
                qmproduction_id.update(qm_production_values)
                _logger.info("Service API : QM Production Updated (%s) (%s)", qmproduction_id.id, action)

        if qmproduction_id:
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'qmproduction_id': qm_production_values,
            })
        else:
            status = 'REJECTED'
            status_code = 400
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': 'Account ID Not Available for Update',
            })
