import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class JournalEntryCreateAPI(models.Model):
    _name = 'journal.entry.api.create'

    @api.model
    def action_create_journal_entry(self, values):
        journal_entry_id = False
        journal_entry_values = {}
        event_type = ''
        _logger.info("Service API : Journal Entry Creation Method ()")

        if 'event_type' in values:
            event_type = values.get('event_type')

        if 'journal_entry_id' in values:
            journal_entry_id = int(values.get('journal_entry_id'))

        if 'name' in values:
            name = values.get('name', False)
            journal_entry_values.update({'name': name or False})

        if 'accounting_date' in values:
            accounting_date = values.get('accounting_date', False)
            journal_entry_values.update({'date': accounting_date or False})

        if 'reference' in values:
            reference = values.get('reference', False)
            journal_entry_values.update({'ref': reference or False})

        if 'journal_id' in values:
            journal_id = int(values.get('journal_id', False))
            journal_entry_values.update({'journal_id': journal_id or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            journal_entry_values.update({'company_id': company_id or False})

        if 'operating_unit_id' in values:
            operating_unit_id = int(values.get('operating_unit_id', False))
            journal_entry_values.update({'operating_unit_id': operating_unit_id or False})

        if 'journal_lines' in values:
            line_items = []
            journal_pos = 0
            journal_lines = values.get('journal_lines')
            for journal in journal_lines:
                tax_ids = []
                journal_line_items = {}
                if 'tax_ids' in journal:
                    tax_string = journal['tax_ids']
                    _logger.info("Service API : Taxes %s", tax_string)
                    if tax_string:
                        tax_list = tax_string.split(',')

                        for tax_id in tax_list:
                            if isinstance(tax_id, int):
                                tax_ids.append(int(tax_id))
                        #    tax_rec = self.env['account.tax'].search([('id', '=', int(tax_id))], limit=1)
                        #    if tax_rec:
                        #        tax_ids.append(tax_id.id)

                    journal_line_items.update({'tax_ids': [(6, 0, tax_ids or [])]})

                journal_line_items.update({'account_id': int(journal['account_id'])})

                if 'partner_id' in journal:
                    journal_line_items.update({'partner_id': int(journal['partner_id'])})
                if 'analytic_account_id' in journal:
                    journal_line_items.update({'analytic_account_id': int(journal['analytic_account_id'])})

                if 'reference' in journal:
                    journal_line_items.update({'name': journal['reference'] or False})
                journal_line_items.update({'debit': float(journal['debit'])})
                journal_line_items.update({'credit': float(journal['credit'])})

                line_items.append((0, journal_pos, journal_line_items))
                journal_pos = journal_pos + 1
            journal_entry_values.update({'line_ids': line_items})

        if event_type == 'create':
            journal_entry_id = self.env['account.move'].create(journal_entry_values)
            journal_entry_id.action_post()
            _logger.info("Service API : Account Move Created (%s )", journal_entry_id.id)
        elif event_type == 'cancel':
            journal_entry_id = self.env['account.move'].search([('id', '=', values.get('journal_entry_id'))])
            if journal_entry_id:
                journal_entry_id.button_draft()
                journal_entry_id.button_cancel()
            _logger.info("Service API : Account Move Cancelled (%s )", journal_entry_id.id)
        elif event_type == 'update':
            journal_entry_id = self.env['account.move'].search([('id', '=', values.get('journal_entry_id'))])
            jounral_entry_line_ids = self.env['account.move.line'].search([('move_id', '=', journal_entry_id.id)])
            _logger.info("Service API : Account Move Live Remove >>>> (%s )", jounral_entry_line_ids)
            if journal_entry_id:
                journal_entry_id.button_draft()

            if jounral_entry_line_ids:
                jounral_entry_line_ids.unlink()
                _logger.info("Service API : Account Move Live Remove <<<< (%s )", jounral_entry_line_ids)

            if journal_entry_id:
                journal_entry_id.update(journal_entry_values)
                journal_entry_id.action_post()
                _logger.info("Service API : Account Move Updated (%s) ", journal_entry_id.id)

        if journal_entry_id:
            _logger.info("Service API : Journal Entry Created (%s)", journal_entry_id)
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'journal_entry_id': journal_entry_id.id,
            })
