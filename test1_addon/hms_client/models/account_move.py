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
    _name = 'account.move.api.create'

    @api.model
    def action_create_move(self, values):
        invoice_vals = {}

        event_type = ''
        invoice_id = 0
        payment_id = False

        if 'event_type' in values:
            event_type = values.get('event_type')

        if 'invoice_id' in values:
            invoice_id = int(values.get('invoice_id'))

        if 'payment_id' in values:
            payment_id = int(values.get('payment_id'))

        if 'partner_id' in values:
            partner_id = int(values.get('partner_id'))
            invoice_vals.update({'partner_id': partner_id or False})

        # if 'name' in values:
        #     name = invoice_vals.get('name', False)
        #     invoice_vals.update({'name': name or False})

        if 'move_type' in values:
            move_type = values.get('move_type', False)
            invoice_vals.update({'move_type': move_type or False})

        if 'invoice_date' in values:
            invoice_date = values.get('invoice_date', False)
            invoice_vals.update({'invoice_date': invoice_date or False})

        if 'invoice_date_due' in values:
            invoice_date_due = values.get('invoice_date_due', False)
            invoice_vals.update({'invoice_date_due': invoice_date_due or False})

        if 'operating_unit_id' in values:
            operating_unit_id = int(values.get('operating_unit_id', False))
            invoice_vals.update({'operating_unit_id': operating_unit_id or False})

        if 'payment_reference' in values:
            payment_reference = values.get('payment_reference', False)
            invoice_vals.update({'payment_reference': payment_reference or False})
        else:
            payment_reference = values.get('name', False)
            invoice_vals.update({'payment_reference': payment_reference or False})

        if 'ref' in values:
            ref = values.get('ref', False)
            invoice_vals.update({'ref': ref or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            invoice_vals.update({'company_id': company_id or False})

        if 'l10n_in_gst_treatment' in values:
            l10n_in_gst_treatment = values.get('l10n_in_gst_treatment', False)
            invoice_vals.update({'l10n_in_gst_treatment': l10n_in_gst_treatment or False})

        if 'journal_id' in values:
            journal_id = int(values.get('journal_id', False))
            invoice_vals.update({'journal_id': journal_id or False})

        if 'invoice_lines' in values:
            invoices = {}

            invoice_lines = values.get('invoice_lines')  # converted
            _logger.info("Service API : Invoice Details (%s)", invoices)
            invoice_pos = 0
            invoice_line_det = []
            for invoice_item in invoice_lines:

                invoice_line_items = {}

                _logger.info("Service API : Invoice Details (%s)", invoice_item)
                if 'tax_ids' in invoice_item:
                    tax_ids = []
                    tax_string = invoice_item['tax_ids']
                    _logger.info("Service API : Taxes String %s", tax_string)
                    if tax_string:
                        tax_list = tax_string.split(',')
                        for tax_id in tax_list:
                            tax_ids.append(int(tax_id))
                        _logger.info("Service API : Tax Id List %s", tax_ids)
                        invoice_line_items.update({'tax_ids': [(6, 0, tax_ids or [])]})

                invoice_line_items.update({'product_id': int(invoice_item['product_id'])})
                invoice_line_items.update({'account_id': int(invoice_item['account_id'])})
                if 'reference' in invoice_item:
                    invoice_line_items.update({'name': invoice_item['reference']})
                else:
                    invoice_line_items.update({'name': '/'})
                if 'discount_percentage' in invoice_item:
                    invoice_line_items.update({'discount': float(invoice_item['discount_percentage'])})
                if 'uom' in invoice_item:
                    invoice_line_items.update({'product_uom_id': invoice_item['uom']})

                invoice_line_items.update({'price_unit': float(invoice_item['price_unit'])})
                invoice_line_items.update({'quantity': float(invoice_item['quantity'])})
                if 'analytic_account_id' in invoice_item:
                    invoice_line_items.update({'analytic_account_id': int(invoice_item['analytic_account_id'])})

                invoice_line_det.append((0, invoice_pos, invoice_line_items))
                invoice_pos = invoice_pos + 1
            _logger.info("Service API : Invoice Lines Details (%s)", invoice_line_det)
            invoice_vals.update({'invoice_line_ids': invoice_line_det})

        account_move_id = False
        action = False
        account_move_line_id = False
        new_payment_id = False

        if event_type == 'create':
            if 'is_round_off' in values:
                is_round_off = values.get('is_round_off')
                rounding_method_val = {}

                if is_round_off == 't':
                    rounding_method_id = False
                    company_id = self.env['res.company'].search([('id', '=', company_id)])
                    rounding_method_name = 'API Round Off-' + str(company_id.id)
                    rounding_method = self.env['account.cash.rounding'].search([('name', '=', rounding_method_name)])
                    if not rounding_method:
                        if 'round_off_account_id' in values:
                            round_off_account_id = int(values.get('round_off_account_id'))
                            self.env.user.company_id = company_id
                            rounding_method_val.update(
                                {'profit_account_id': round_off_account_id, 'loss_account_id': round_off_account_id,
                                 'name': rounding_method_name, 'strategy': 'global_fixed'})
                            rounding_method = self.env['account.cash.rounding'].create(rounding_method_val)
                            rounding_method_id = rounding_method.id
                    else:
                        rounding_method_id = rounding_method.id
                    if 'round_off_value' in values:
                        invoice_vals.update({'invoice_cash_rounding_id': rounding_method_id,
                                             'round_off_amount': values.get('round_off_value')
                                             })
            _logger.info("Service API : Invoice Vals - Create (%s)", invoice_vals)
            account_move_id = self.env['account.move'].create(invoice_vals)
            account_move_id.action_post()
            if 'name' in values:
                name = values.get('name', False)
                res = account_move_id.write({'name': name})
                _logger.info("Service API : Account Move Created (%s ) (%s)", account_move_id.id, res)
            if 'is_payment' in values:
                is_payment = values.get('is_payment')
                payment_vals = {}
                if is_payment == 't':
                    if 'payment_journal_id' in values:
                        payment_journal_id = int(values.get('payment_journal_id', False))
                        payment_vals.update({'journal_id': payment_journal_id or False})
                    if account_move_id.invoice_date:
                        payment_date = account_move_id.invoice_date
                        payment_vals.update({'payment_date': payment_date or False})
                    if account_move_id.amount_total:
                        amount_total = account_move_id.amount_total
                        payment_vals.update({'amount': amount_total})
                    if 'payment_reference' in values:
                        payment_reference = values.get('payment_reference', False)
                    else:
                        payment_reference = values.get('name', False)
                    payment_vals.update({'communication': payment_reference})
                    payment_vals.update({'partner_type': 'customer'})
                    payment_vals.update({'payment_type': 'outbound'})
                    new_payment_id = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                       active_ids=account_move_id.ids).create(
                        payment_vals)
                    new_payment_id.action_create_payments()
                    _logger.info("Service API : Payment Created (%s )", new_payment_id.id)

        elif event_type == 'cancel':
            account_move_id = self.env['account.move'].search([('id', '=', values.get('invoice_id'))])
            if account_move_id:
                account_move_id.button_draft()
                account_move_id.button_cancel()
            if payment_id:
                payment_id = self.env['account.payment'].search([('id', '=', payment_id)])
                payment_id.action_draft()
                payment_id.action_cancel()
            _logger.info("Service API : Account Move Cancelled (%s )", account_move_id.id)

        elif event_type == 'update':
            account_move_id = self.env['account.move'].search([('id', '=', values.get('invoice_id'))])
            account_move_line_ids = self.env['account.move.line'].search([('move_id', '=', account_move_id.id)])
            _logger.info("Service API : Account Move Live Remove >>>> (%s )", account_move_line_ids)
            if account_move_id:
                account_move_id.button_draft()

            if account_move_line_ids:
                account_move_line_ids.unlink()
                _logger.info("Service API : Account Move Live Remove <<<< (%s )", account_move_line_ids)

            if payment_id:
                done_payment_id = self.env['account.payment'].search([('id', '=', payment_id)])
                if done_payment_id:
                    done_payment_id.action_draft()
                    done_payment_id.action_cancel()
                    _logger.info("Service API : Account Payment  (%s) Deleted ", done_payment_id.id)

            if account_move_id:
                _logger.info("Service API : Account Move Starting Update (%s)", account_move_id.id)
                if 'is_round_off' in values:
                    is_round_off = values.get('is_round_off')
                    rounding_method_val = {}
                    if is_round_off == 't':
                        rounding_method_id = False
                        company_id = self.env['res.company'].search([('id', '=', company_id)])
                        rounding_method_name = 'API Round Off-' + str(company_id.id)
                        rounding_method = self.env['account.cash.rounding'].search([('name', '=',rounding_method_name)])
                        if not rounding_method:
                            if 'round_off_account_id' in values:
                                round_off_account_id = int(values.get('round_off_account_id'))
                                self.env.user.company_id = company_id
                                rounding_method_val.update(
                                    {'profit_account_id': round_off_account_id, 'loss_account_id': round_off_account_id,
                                     'name': rounding_method_name, 'strategy': 'global_fixed'})
                                rounding_method = self.env['account.cash.rounding'].create(rounding_method_val)
                                rounding_method_id = rounding_method.id
                        else:
                            rounding_method_id = rounding_method.id
                        if 'round_off_value' in values:
                            account_move_id.write({'invoice_cash_rounding_id': rounding_method_id,
                                                   'round_off_amount': values.get('round_off_value')
                                                   })
                _logger.info("Service API : Invoice Vals - update (%s)", invoice_vals)
                account_move_id.update(invoice_vals)
                if 'name' in values:
                    name = values.get('name', False)
                    res = account_move_id.write({'name': name})

                account_move_id.action_post()
                _logger.info("Service API : Account Move Updated (%s) (%s)", account_move_id.id, action)
                if 'is_payment' in values:
                    is_payment = values.get('is_payment')
                    payment_vals = {}
                    if is_payment == 't':
                        if 'payment_journal_id' in values:
                            payment_journal_id = int(values.get('payment_journal_id', False))
                            payment_vals.update({'journal_id': payment_journal_id or False})
                        if account_move_id.invoice_date:
                            payment_date = account_move_id.invoice_date
                            payment_vals.update({'payment_date': payment_date or False})
                        if account_move_id.amount_total:
                            amount_total = account_move_id.amount_total
                            payment_vals.update({'amount': amount_total})
                        if 'payment_reference' in values:
                            payment_reference = values.get('payment_reference', False)
                        else:
                            payment_reference = values.get('name', False)
                        payment_vals.update({'communication': payment_reference})
                        payment_vals.update({'partner_type': 'customer'})
                        payment_vals.update({'payment_type': 'outbound'})
                        new_payment_id = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                           active_ids=account_move_id.ids).create(
                            payment_vals)
                        new_payment_id.action_create_payments()

        if account_move_id:
            if new_payment_id and account_move_id:
                _logger.info("Service API : Account Move and Payment Created (%s,%s)", account_move_id.id,
                             new_payment_id.id)
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'account_move_id': account_move_id.id,
                    'payment_id': new_payment_id.id,
                    'dbname': self._cr.dbname,
                })
            else:
                _logger.info("Service API : Account Move Created (%s)", account_move_id.id)
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'account_move_id': account_move_id.id,
                    'dbname': self._cr.dbname,
                })
