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
    _name = 'coa.api.create'

    @api.model
    def action_create_coa(self, values):

        event_type = ''
        account_id = False
        account_vals = {}
        account_update_vals = {}

        if 'event_type' in values:
            event_type = values.get('event_type')

        if 'account_id' in values:
            account_id = int(values.get('account_id'))

        # Following Check To be Enabled
        # if event_type == 'update' and account_id == False:
        #    status = 'REJECTED'
        #    status_code = 400
        #    return json.dumps({
        #        'status': status,
        #        'status_code': status_code,
        #        'Error': 'Account ID not available',
        #    })

        if 'code' in values:
            code = values.get('code', False)
            account_vals.update({'code': code or False})

        if 'name' in values:
            name = values.get('name', False)
            account_vals.update({'name': name or False})
            account_update_vals.update({'name': name or False})

        if 'user_type_id' in values:
            type = int(values.get('user_type_id', False))
            account_vals.update({'user_type_id': type or False})
            account_update_vals.update({'user_type_id': type or False})

        if 'tax_ids' in values:
            tax_ids = values.get('tax_ids', False)
            account_vals.update({'tax_ids': tax_ids or False})

        if 'allowed_journal_ids' in values:
            allowed_journal_ids = values.get('allowed_journal_ids', False)
            account_vals.update({'allowed_journal_ids': allowed_journal_ids or False})

        if 'group_id' in values:
            group_id = values.get('group_id', False)
            account_vals.update({'group_id': group_id or False})
            account_update_vals.update({'group_id': group_id or False})

        if 'reconcile' in values:
            reconcile = values.get('reconcile', False)
            account_vals.update({'reconcile': reconcile or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            account_vals.update({'company_id': company_id or False})

        if event_type == 'create':
            account_id = self.env['account.account'].create(account_vals)
            if account_id:
                _logger.info("Service API : Account Created")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'account_id': account_id.id,
                })
        elif event_type == 'update':
            account_id = self.env['account.account'].search([('id', '=', values.get('account_id'))])
            if account_id:
                account_id.update(account_update_vals)
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'account_id': account_id.id,
                })
            else:
                status = 'REJECTED'
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': 'Account ID Not Available for Update',
                })
        else:
            status = 'REJECTED'
            status_code = 400
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': 'Invalid Event Type'
            })


class AccountSearchAPI(models.Model):
    _name = 'coa.api.search'

    @api.model
    def action_search_coa(self, vals):
        account = self.env['account.account'].browse(vals['account_id'])
        if account:
            _logger.info("Service API : Account Verified")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'account_id': account.id,
                # 'dbname': self._cr.dbname,

            })
