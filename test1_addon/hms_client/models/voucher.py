import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class InvoiceCreateAPI(models.Model):
    _name = 'voucher.api.create'

    @api.model
    def action_create_voucher(self, values):
        bank_receipt_values = {}
        bank_payment_values = {}
        cash_receipt_values = {}
        cash_payment_values = {}
        event_type = ''

        if 'event_type' in values:
            event_type = values.get('event_type')

        if 'name' in values:
            name = values.get('name', False)
            bank_receipt_values.update({'name': name or False})
            bank_payment_values.update({'name': name or False})
            cash_receipt_values.update({'name': name or False})
            cash_payment_values.update({'name': name or False})

        if 'date' in values:
            date = values.get('date', False)
            bank_receipt_values.update({'date': date or False})
            bank_payment_values.update({'date': date or False})
            cash_receipt_values.update({'date': date or False})
            cash_payment_values.update({'date': date or False})

        if 'received_from' in values:
            received_from = values.get('received_from', False)
            bank_receipt_values.update({'received_from': received_from or False})
            cash_receipt_values.update({'received_from': received_from or False})

        if 'paid_to' in values:
            paid_to = values.get('paid_to', False)
            bank_payment_values.update({'paid_to': paid_to or False})
            cash_payment_values.update({'paid_to': paid_to or False})

        if 'cheque_no' in values:
            cheque_no = values.get('cheque_no', False)
            bank_receipt_values.update({'cheque_no': cheque_no or False})
            bank_payment_values.update({'cheque_no': cheque_no or False})

        if 'cheque_date' in values:
            cheque_date = values.get('cheque_date', False)
            bank_receipt_values.update({'cheque_date': cheque_date or False})
            bank_payment_values.update({'cheque_date': cheque_date or False})

        if 'ref' in values:
            ref = values.get('ref', False)
            bank_receipt_values.update({'ref': ref or False})
            bank_payment_values.update({'ref': ref or False})
            cash_receipt_values.update({'ref': ref or False})
            cash_payment_values.update({'ref': ref or False})

        if 'journal_id' in values:
            journal_id = int(values.get('journal_id', False))
            bank_receipt_values.update({'journal_id': journal_id or False})
            bank_payment_values.update({'journal_id': journal_id or False})
            cash_receipt_values.update({'journal_id': journal_id or False})
            cash_payment_values.update({'journal_id': journal_id or False})

        if 'account_id' in values:
            account_id = int(values.get('account_id', False))
            bank_receipt_values.update({'account_id': account_id or False})
            bank_payment_values.update({'account_id': account_id or False})
            cash_receipt_values.update({'account_id': account_id or False})
            cash_payment_values.update({'account_id': account_id or False})

        if 'amount' in values:
            amount = values.get('amount', False)
            bank_receipt_values.update({'amount': amount or False})
            bank_payment_values.update({'amount': amount or False})
            cash_receipt_values.update({'amount': amount or False})
            cash_payment_values.update({'amount': amount or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            bank_receipt_values.update({'company_id': company_id or False})
            bank_payment_values.update({'company_id': company_id or False})
            cash_receipt_values.update({'company_id': company_id or False})
            cash_payment_values.update({'company_id': company_id or False})

        if 'operating_unit_id' in values:
            operating_unit_id = int(values.get('operating_unit_id', False))
            bank_receipt_values.update({'operating_unit_id': operating_unit_id or False})
            bank_payment_values.update({'operating_unit_id': operating_unit_id or False})
            cash_payment_values.update({'operating_unit_id': operating_unit_id or False})
            cash_receipt_values.update({'operating_unit_id': operating_unit_id or False})

        voucher_pos = 0
        if 'line_ids' in values:
            line_items = []
            for i in values.get('line_ids'):
                account_dict = {}

                account_dict.update({'account_id': int(i['account_id'])})
                if 'partner_id' in i:
                    account_dict.update({'partner_id': int(i['partner_id'])})
                if 'analytic_account_id' in i:
                    account_dict.update({'analytic_account_id': int(i['analytic_account_id'])})

                # taxes = False
                # for tax in taxes:
                #    tax_list = tax['tax_names'].split(',')
                #    if i['tax'] in tax_list:
                #        account_dict['tax_ids'] = tax['tax_id']
                account_dict['name'] = i['description']
                account_dict['debit'] = float(i['debit'])
                account_dict['credit'] = float(i['credit'])
                line_items.append((0, voucher_pos, account_dict))
                voucher_pos = voucher_pos + 1
            bank_receipt_values.update({'line_ids': line_items})
            bank_payment_values.update({'line_ids': line_items})
            cash_receipt_values.update({'line_ids': line_items})
            cash_payment_values.update({'line_ids': line_items})

        if event_type == 'create':
            if 'voucher_type' in values:
                if values.get('voucher_type') == 'bank_receipt':
                    bank_receipt = self.env['bank.receipt'].create(bank_receipt_values)
                    bank_receipt.action_validate()
                    bank_receipt.action_done()
                    if bank_receipt:
                        _logger.info("Service API : Bank Receipt Voucher Created")
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'voucher_id': bank_receipt.id,
                        })

                if values.get('voucher_type') == 'bank_payment':
                    bank_payment = self.env['bank.payment'].create(bank_payment_values)
                    bank_payment.action_validate()
                    bank_payment.action_done()
                    if bank_payment:
                        _logger.info("Service API : Bank Payment Voucher Created")
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'voucher_id': bank_payment.id,
                        })

                if values.get('voucher_type') == 'cash_receipt':
                    cash_receipt = self.env['cash.receipt'].create(cash_receipt_values)
                    cash_receipt.action_validate()
                    cash_receipt.action_done()
                    if cash_receipt:
                        _logger.info("Service API : Cash receipt Voucher Created")
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'voucher_id': cash_receipt.id,
                        })

                if values.get('voucher_type') == 'cash_payment':
                    cash_payment = self.env['cash.payment'].create(cash_payment_values)
                    cash_payment.action_validate()
                    cash_payment.action_done()
                    if cash_payment:
                        _logger.info("Service API : Cash Payment Created")
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'voucher_id': cash_payment.id,
                        })

        elif event_type == "update":
            voucher_id = False
            if 'voucher_type' in values:
                if values.get('voucher_type') == 'bank_payment':
                    voucher_id = self.env['bank.payment'].search([('id', '=', int(values.get('voucher_id')))])
                    if voucher_id:
                        voucher_id.button_draft()

                    if 'line_ids' in values:
                        voucher_id.line_ids.unlink()
                        voucher_id.update(bank_payment_values)
                        voucher_id.action_validate()

            if 'voucher_type' in values:
                if values.get('voucher_type') == 'bank_receipt':

                    voucher_id = self.env['bank.receipt'].search([('id', '=', int(values.get('voucher_id')))])

                    if voucher_id:
                        voucher_id.button_draft()
                    if 'line_ids' in values:
                        voucher_id.line_ids.unlink()
                        voucher_id.update(bank_receipt_values)
                        voucher_id.action_validate()
                        voucher_id.action_done()

            if 'voucher_type' in values:
                if values.get('voucher_type') == 'cash_receipt':
                    voucher_id = self.env['cash.receipt'].search([('id', '=', int(values.get('voucher_id')))])
                    if voucher_id:
                        voucher_id.button_draft()
                    if 'line_ids' in values:
                        voucher_id.line_ids.unlink()
                        voucher_id.update(cash_receipt_values)
                        voucher_id.action_validate()
                        voucher_id.action_done()

            if 'voucher_type' in values:
                if values.get('voucher_type') == 'cash_payment':
                    voucher_id = self.env['cash.payment'].search([('id', '=', int(values.get('voucher_id')))])
                    if voucher_id:
                        voucher_id.button_draft()

                    if 'line_ids' in values:
                        voucher_id.line_ids.unlink()
                        voucher_id.update(cash_payment_values)
                        voucher_id.action_validate()
                        voucher_id.action_done()

            if voucher_id:
                _logger.info("Service API : Bank Payment Voucher Created")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'voucher_id': voucher_id.id,
                })

        elif event_type == 'cancel':
            if 'voucher_type' in values:
                if values.get('voucher_type') == 'bank_payment':
                    voucher_id = self.env['bank.payment'].search([('id', '=', values.get('voucher_id'))])
                    if voucher_id:
                        voucher_id.button_draft()
                        voucher_id.action_cancel()
                        _logger.info("Service API : Bank Payment Cancelled (%s )", voucher_id.id)
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'voucher_id': voucher_id.id,
                        })

                if values.get('voucher_type') == 'bank_receipt':
                    voucher_id = self.env['bank.receipt'].search([('id', '=', values.get('voucher_id'))])
                    if voucher_id:
                        voucher_id.button_draft()
                        voucher_id.action_cancel()
                        _logger.info("Service API : Bank Receipt Cancelled (%s )", voucher_id.id)
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'voucher_id': voucher_id.id,
                        })

                if values.get('voucher_type') == 'cash_receipt':
                    voucher_id = self.env['cash.receipt'].search([('id', '=', values.get('voucher_id'))])
                    if voucher_id:
                        voucher_id.button_draft()
                        voucher_id.action_cancel()
                        _logger.info("Service API : Cash Receipt Cancelled (%s )", voucher_id.id)
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'voucher_id': voucher_id.id,
                        })

                if values.get('voucher_type') == 'cash_payment':
                    voucher_id = self.env['cash.payment'].search([('id', '=', values.get('voucher_id'))])
                    if voucher_id:
                        voucher_id.button_draft()
                        voucher_id.action_cancel()
                        _logger.info("Service API : Cash Payment Cancelled (%s )", voucher_id.id)
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'voucher_id': voucher_id.id,
                        })
