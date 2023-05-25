import json
import logging
from odoo import _, api, fields, models

from datetime import datetime

_logger = logging.getLogger(__name__)


class PaymentCreateAPI(models.Model):
    _name = 'account.payment.api.create'

    @api.model
    def action_create_payment(self, values):
        payment_vals = {}

        payment_id = 0

        event_type = ''
        journal_id = False

        if 'event_type' in values:
            event_type = values.get('event_type')

        if 'payment_id' in values:
            payment_id = int(values.get('payment_id'))

        if 'payment_type' in values:
            payment_type = values.get('payment_type', False)
            payment_vals.update({'payment_type': payment_type or False})

        if 'payment_reference' in values:
            payment_reference = values.get('payment_reference', False)
            payment_vals.update({'ref': payment_reference or False})

        if 'name' in values:
            name = values.get('name', False)
            payment_vals.update({'name': name or False})

        if 'partner_type' in values:
            partner_type = values.get('partner_type', False)
            payment_vals.update({'partner_type': partner_type or False})

        if 'amount' in values:
            amount = values.get('amount', False)
            payment_vals.update({'amount': amount or False})

        if 'date' in values:
            date = values.get('date', False)
            payment_vals.update({'date': date or False})

        if 'journal_id' in values:
            journal_id = int(values.get('journal_id', False))
            journal = self.env['account.journal'].search([('id', '=', journal_id)])
            if journal.type == 'bank' or journal.type == 'cash':
                payment_vals.update({'journal_id': journal_id or False})
            else:
                status = 'REJECTED'
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': 'Journal type must be Bank or Cash'
                })

        if 'operating_unit_id' in values:
            operating_unit_id = int(values.get('operating_unit_id', False))
            payment_vals.update({'operating_unit_id': operating_unit_id or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            payment_vals.update({'company_id': company_id or False})

        if event_type == 'create':
            payment_id = False
            if values['is_internal_transfer'] == "true":
                journal = self.env['account.journal'].search([('id', '=', journal_id)])
                destination_account_id = journal.company_id.transfer_account_id
                company_id = int(payment_vals.get('company_id', False))
                company = self.env['res.company'].search([('id', '=', company_id)])
                company_partner_id = company.partner_id.id
                if company_partner_id:
                    payment_vals.update({"partner_id": company_partner_id or False})
                if 'destination_journal_id' in values:
                    destination_journal_id = int(values.get('destination_journal_id', False))
                    journal = self.env['account.journal'].search([('id', '=', destination_journal_id)])
                    if journal.type == 'bank' or journal.type == "cash":
                        payment_vals.update({'destination_journal_id': destination_journal_id})
                    else:
                        _logger.info("Service API : Payment cannot created destination journal must be Bank or Cash")
                        status = 'REJECTED'
                        status_code = 400
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'msg': 'Destination Journal type must be Bank or Cash'
                        })

                if destination_account_id:
                    payment_vals.update({'destination_account_id': destination_account_id.id})
                payment_id = self.env['account.payment'].create(payment_vals)
                payment_id.action_post()

            if (values['is_internal_transfer']) == "false":
                if 'destination_account' in values:
                    account_id = int(values.get('destination_account', False))
                    payment_vals.update({'destination_account_id': account_id or False})
                if 'partner_id' in values:
                    partner_id = int(values.get('partner_id', False))
                    payment_vals.update({'partner_id': partner_id or False})
                payment_id = self.env['account.payment'].create(payment_vals)
                payment_id.action_post()

            if payment_id:
                _logger.info("Service API : Payment Created")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'payment_id': payment_id.id,
                })

        if event_type == 'cancel':
            payment = self.env['account.payment'].search([('id', '=', payment_id)])
            if payment and payment.state == 'posted':
                if values['is_internal_transfer'] == "false":
                    payment.move_id.button_draft()
                    payment.move_id.button_cancel()
                    _logger.info("Service API : Payment cancelled (%s)", payment_id)

                if values['is_internal_transfer'] == "true":
                    journal_entry=False
                    ids = []
                    move_line_ids = payment.move_id.line_ids
                    for aml in move_line_ids:
                        if aml.account_id.reconcile:
                            ids.extend([r.debit_move_id.id for r in
                                        aml.matched_debit_ids] if aml.credit > 0 else [
                                r.credit_move_id.id for r in aml.matched_credit_ids])
                            ids.append(aml.id)
                    for val in ids:
                        journal_entry = self.env['account.move.line'].search([('id', '=', val)])
                        if journal_entry:
                            journal_entry.move_id.button_draft()
                            journal_entry.move_id.button_cancel()
                    if journal_entry:
                        _logger.info("Service API : Account Move Cancelled (%s )", journal_entry)
                        _logger.info("Service API : Payment cancelled")
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'payment_id': (payment_id, "cancelled")
                        })
            else:
                _logger.info("Service API : No Corresponding Payment Id or this payment is already Cancelled")
