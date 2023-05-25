import json
import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class InvoiceBillCreateAPI(models.Model):
    _name = 'invoice.bill.api.create'

    @api.model
    def action_invoice_bill_create(self, vals):

        invoice = {}
        bill = {}

        if 'company_id' in vals:
            company_id = int(vals.get('company_id', False))
            bill.update({'company_id': company_id or False})
            invoice.update({'company_id': company_id or False})

        if 'operating_unit_id' in vals:
            operating_unit_id = int(vals.get('operating_unit_id', False))
            bill.update({'operating_unit_id': operating_unit_id or False})
            invoice.update({'operating_unit_id': operating_unit_id or False})

        # if 'gst_treatment' in vals:
        #     l10n_in_gst_treatment = (vals.get('gst_treatment', False))
        #     bill.update({'l10n_in_gst_treatment': l10n_in_gst_treatment or False})
        #     invoice.update({'l10n_in_gst_treatment': l10n_in_gst_treatment or False})

        if 'invoice_date' in vals:
            invoice_date = (vals.get('invoice_date', False))
            bill.update({'invoice_date': invoice_date or False})
            invoice.update({'invoice_date': invoice_date or False})

        if 'invoice_date_due' in vals:
            invoice_date_due = vals.get('invoice_date_due', False)
            bill.update({'invoice_date_due': invoice_date_due or False})
            invoice.update({'invoice_date_due': invoice_date_due or False})

        if 'accounting_date' in vals:
            date = (vals.get('accounting_date', False))
            bill.update({'date': date or False})
            invoice.update({'date': date or False})

        if 'event_type' in vals:
            event_type = (vals.get('event_type'))
            if event_type == 'create':
                if 'mode' in vals:
                    mode = (vals.get('mode'))
                    if mode == 'bill':
                        if 'purchase_order_id' in vals:
                            purchase_order_id = int(vals.get('purchase_order_id'))
                            purchaseorder = self.env['purchase.order'].browse(purchase_order_id)
                            purchase_pdt = []
                            for res in purchaseorder.order_line.product_id:
                                purchase_pdt.append(res.id)
                            order_line_pdt = []
                            if 'order_lines' in vals:
                                checkpdt = vals.get('order_lines')
                                for pdt in checkpdt:
                                    order_line_pdt.append(int(pdt['product_id']))
                            if all(x in purchase_pdt for x in order_line_pdt):
                                old_bills = []
                                bill_search = self.env['account.move'].search(
                                    [("purchase_id", "=", purchase_order_id)])
                                for i in bill_search:
                                    old_bills.append(str(i.id))
                                purchaseorder.action_create_invoice()
                                bills_odd = []
                                bill_search_confirm = self.env['account.move'].search(
                                    [("purchase_id", "=", purchase_order_id)])
                                for i in bill_search_confirm:
                                    bills_odd.append(str(i.id))
                                last_bill = set(bills_odd).difference(old_bills)
                                bill_int = ''.join(last_bill)
                                account_mov = self.env['account.move'].browse(int(bill_int))
                                if account_mov:
                                    if 'order_lines' in vals:
                                        order_lines = vals.get('order_lines')
                                        invoice_pos = 0
                                        invoice_line_det = [(5, 0, 0)]
                                        for invoice_item in order_lines:
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
                                                    invoice_line_items.update(
                                                        {'tax_ids': [(6, 0, tax_ids or [])]})

                                            invoice_line_items.update(
                                                {'product_id': int(invoice_item['product_id'])})
                                            invoice_line_items.update(
                                                {'account_id': int(invoice_item['account_id'])})
                                            for rec in purchaseorder.order_line:
                                                if int(invoice_item['product_id']) == rec.product_id.id:
                                                    invoice_line_items.update({'purchase_line_id': rec.id})
                                                else:
                                                    _logger.info(
                                                        "Service API : Product does not exist on SaleOrder")

                                            if 'reference' in invoice_item:
                                                invoice_line_items.update({'name': invoice_item['reference']})
                                            else:
                                                invoice_line_items.update({'name': '/'})
                                            if 'uom' in invoice_item:
                                                invoice_line_items.update(
                                                    {'product_uom_id': invoice_item['uom']})
                                            invoice_line_items.update(
                                                {'price_unit': float(invoice_item['price_unit'])})
                                            invoice_line_items.update(
                                                {'quantity': float(invoice_item['quantity'])})
                                            if 'analytic_account_id' in invoice_item:
                                                invoice_line_items.update(
                                                    {'analytic_account_id': int(
                                                        invoice_item['analytic_account_id'])})

                                            invoice_line_det.append((0, invoice_pos, invoice_line_items))
                                            invoice_pos = invoice_pos + 1
                                        _logger.info("Service API : Invoice Lines Details (%s)",
                                                     invoice_line_det)
                                        bill.update({'invoice_line_ids': invoice_line_det})
                                        if 'is_round_off' in vals:
                                            is_round_off = vals.get('is_round_off')
                                            rounding_method_val = {}

                                            if is_round_off == 't':
                                                rounding_method_id = False
                                                company_id = self.env['res.company'].search([('id', '=', company_id)])
                                                rounding_method_name = 'API Round Off-' + str(company_id.id)
                                                rounding_method = self.env['account.cash.rounding'].search(
                                                    [('name', '=', rounding_method_name)])
                                                if not rounding_method:
                                                    if 'round_off_account_id' in vals:
                                                        round_off_account_id = int(vals.get('round_off_account_id'))
                                                        self.env.user.company_id = company_id
                                                        rounding_method_val.update(
                                                            {'profit_account_id': round_off_account_id,
                                                             'loss_account_id': round_off_account_id,
                                                             'name': rounding_method_name, 'strategy': 'global_fixed'})
                                                        rounding_method = self.env['account.cash.rounding'].create(
                                                            rounding_method_val)
                                                        rounding_method_id = rounding_method.id
                                                else:
                                                    rounding_method_id = rounding_method.id
                                                if 'round_off_value' in vals:
                                                    bill.update({'invoice_cash_rounding_id': rounding_method_id,
                                                                       'round_off_amount': vals.get(
                                                                           'round_off_value')
                                                                       })
                                    account_mov.update(bill)
                                    if 'gst_treatment' in vals:
                                        account_mov.write({
                                            'l10n_in_gst_treatment': (vals.get('gst_treatment', False))
                                        })
                                    account_mov.action_post()

                                _logger.info("Service API : Bill Created")
                                status = 'SUCCESS'
                                status_code = 200
                                return json.dumps({
                                    'status': status,
                                    'status_code': status_code,
                                    'invoice': False,
                                    'bill': str(bill_int),
                                    'sale_order_id': False,
                                    'purchase_order_id': str(purchaseorder.id),
                                })

                            else:
                                _logger.info("Service API : Product does not exist on PurchaseOrder")
                                status = 'FAILED'
                                status_code = 400
                                return json.dumps({
                                    'status': status,
                                    'status_code': status_code,
                                    'invoice': False,
                                    'bill': False,
                                    'sale_order_id': False,
                                    'purchase_order_id': str(purchaseorder.id),

                                })

                    if mode == 'invoice':
                        if 'sale_order_id' in vals:
                            sale_order_id = int(vals.get('sale_order_id'))
                            saleorder = self.env['sale.order'].browse(sale_order_id)
                            sale_pdt = []
                            for res in saleorder.order_line.product_id:
                                sale_pdt.append(res.id)
                            order_line_pdt = []
                            if 'order_lines' in vals:
                                checkpdt = vals.get('order_lines')
                                for pdt in checkpdt:
                                    order_line_pdt.append(int(pdt['product_id']))
                            if all(x in sale_pdt for x in order_line_pdt):
                                if saleorder.state == 'sale':
                                    invoice_obj = saleorder._create_invoices()

                                    if 'order_lines' in vals:
                                        order_lines = vals.get('order_lines')
                                        invoice_pos = 0
                                        invoice_line_det = [(5, 0, 0)]
                                        for invoice_item in order_lines:
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
                                            for rec in saleorder.order_line:
                                                if int(invoice_item['product_id']) == rec.product_id.id:
                                                    saleids = []
                                                    saleids.append(rec.id)
                                                    invoice_line_items.update(
                                                        {'sale_line_ids': [(6, 0, saleids or [])]})

                                            if 'reference' in invoice_item:
                                                invoice_line_items.update({'name': invoice_item['reference']})
                                            else:
                                                invoice_line_items.update({'name': '/'})
                                            if 'uom' in invoice_item:
                                                invoice_line_items.update({'product_uom_id': invoice_item['uom']})

                                            invoice_line_items.update({'price_unit': float(invoice_item['price_unit'])})
                                            invoice_line_items.update({'quantity': float(invoice_item['quantity'])})
                                            if 'analytic_account_id' in invoice_item:
                                                invoice_line_items.update(
                                                    {'analytic_account_id': int(invoice_item['analytic_account_id'])})

                                            invoice_line_det.append((0, invoice_pos, invoice_line_items))
                                            invoice_pos = invoice_pos + 1
                                        _logger.info("Service API : Invoice Lines Details (%s)", invoice_line_det)
                                        invoice.update({'invoice_line_ids': invoice_line_det})
                                        if 'is_round_off' in vals:
                                            is_round_off = vals.get('is_round_off')
                                            rounding_method_val = {}

                                            if is_round_off == 't':
                                                rounding_method_id = False
                                                company_id = self.env['res.company'].search([('id', '=', company_id)])
                                                rounding_method_name = 'API Round Off-' + str(company_id.id)
                                                rounding_method = self.env['account.cash.rounding'].search(
                                                    [('name', '=', rounding_method_name)])
                                                if not rounding_method:
                                                    if 'round_off_account_id' in vals:
                                                        round_off_account_id = int(vals.get('round_off_account_id'))
                                                        self.env.user.company_id = company_id
                                                        rounding_method_val.update(
                                                            {'profit_account_id': round_off_account_id,
                                                             'loss_account_id': round_off_account_id,
                                                             'name': rounding_method_name, 'strategy': 'global_fixed'})
                                                        rounding_method = self.env['account.cash.rounding'].create(
                                                            rounding_method_val)
                                                        rounding_method_id = rounding_method.id
                                                else:
                                                    rounding_method_id = rounding_method.id
                                                if 'round_off_value' in vals:
                                                    invoice.update({'invoice_cash_rounding_id': rounding_method_id,
                                                                         'round_off_amount': vals.get(
                                                                             'round_off_value')
                                                                         })
                                        invoice_obj.update(invoice)
                                        if 'gst_treatment' in vals:
                                            invoice_obj.write({
                                                'l10n_in_gst_treatment': (vals.get('gst_treatment', False))
                                            })
                                        invoice_obj.action_post()

                                    _logger.info("Service API : Invoice Created")
                                    status = 'SUCCESS'
                                    status_code = 200
                                    return json.dumps({
                                        'status': status,
                                        'status_code': status_code,
                                        'invoice': str(invoice_obj.id),
                                        'bill': False,
                                        'sale_order_id': str(saleorder.id),
                                        'purchase_order_id': False,

                                    })
                                else:
                                    _logger.info("Service API : SaleOrder is not Confirmed")
                            else:
                                _logger.info("Service API : Product does not exist on SaleOrder")
                                status = 'FAILED'
                                status_code = 400
                                return json.dumps({
                                    'status': status,
                                    'status_code': status_code,
                                    'invoice': False,
                                    'bill': False,
                                    'sale_order_id': str(saleorder.id),
                                    'purchase_order_id': False,

                                })
