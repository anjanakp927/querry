import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class TaxCreateAPI(models.Model):
    _name = 'tax.api.create'

    @api.model
    def action_create_tax(self, values):
        tax_vals = {}

        if 'name' in values:
            name = values.get('name', False)
            tax_vals.update({'name': name or False})

        if 'type_tax_use' in values:
            type_tax_use = values.get('type_tax_use', False)
            tax_vals.update({'type_tax_use': type_tax_use or False})

        if 'amount_type' in values:
            amount_type = values.get('amount_type', False)
            tax_vals.update({'amount_type': amount_type or False})

        if 'amount' in values:
            amount = float(values.get('amount', False))
            tax_vals.update({'amount': amount or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            tax_vals.update({'company_id': company_id or False})

        if 'label_on_invoice' in values:
            label_on_invoice = values.get('label_on_invoice', False)
            tax_vals.update({'description': label_on_invoice or False})

        if 'tax_group' in values :
            tax_group = values.get('tax_group', False)
            tax_group_id = self.env['account.tax.group'].search([('name', '=', tax_group)])
            if not tax_group_id:
                tax_group_id = self.env['account.tax.group'].create({'name': tax_group})
            tax_vals.update({'tax_group_id': tax_group_id.id or False})

        if 'invoice_distribution' in values:
            invoices = {}
            invoice_tax_pos = 0
            invoice_line_det = []
            invoice_distribution = values.get('invoice_distribution',False)
            _logger.info("Service API : Invoice Details (%s)", invoice_distribution)

        invoice_repartition_line_ids = {}
        invoice_repartition_line_ids.update({'repartition_type': 'base'})
        invoice_repartition_line_ids.update({'factor_percent': '0'})
        invoice_line_det.append((0, invoice_tax_pos, invoice_repartition_line_ids))
        invoice_tax_pos = invoice_tax_pos + 1

        for invoice_tax_item in invoice_distribution:
            invoice_repartition_line_ids = {}
            _logger.info("Service API : Invoice Details (%s)",invoice_tax_item)

            invoice_repartition_line_ids.update({'factor_percent':float(invoice_tax_item['factor_percent'])})
            invoice_repartition_line_ids.update({'repartition_type': invoice_tax_item['repartition_type']})
            invoice_repartition_line_ids.update({'account_id': int(invoice_tax_item['account_id'])})
            #invoice_repartition_line_ids.update({'tag_ids': invoice_tax_item['tag_ids']})
            invoice_repartition_line_ids.update({'use_in_tax_closing': invoice_tax_item['use_in_tax_closing']})
            invoice_line_det.append((0, invoice_tax_pos, invoice_repartition_line_ids))
            invoice_tax_pos = invoice_tax_pos + 1

        _logger.info("Service API : Invoice Lines (%s)",invoice_line_det)
        tax_vals.update({'invoice_repartition_line_ids': invoice_line_det})

        if 'refund_distribution' in values:
            invoices = {}
            credit_tax_pos = 0
            refund_line_det = []
            refund_distribution = values.get('refund_distribution', False)
            _logger.info("Service API : Invoice Details (%s)", refund_distribution)

        refund_repartition_line_ids = {}
        refund_repartition_line_ids.update({'repartition_type': 'base'})
        refund_repartition_line_ids.update({'factor_percent': '0'})
        refund_line_det.append((0, credit_tax_pos, refund_repartition_line_ids))
        credit_tax_pos = credit_tax_pos + 1

        for refund_tax_item in refund_distribution:
            refund_repartition_line_ids = {}
            _logger.info("Service API : Invoice Details (%s)",invoice_tax_item)
            refund_repartition_line_ids.update({'factor_percent':float(refund_tax_item['factor_percent'])})
            refund_repartition_line_ids.update({'repartition_type': refund_tax_item['repartition_type']})
            refund_repartition_line_ids.update({'account_id': int(refund_tax_item['account_id'])})
            #refund_repartition_line_ids.update({'tag_ids': refund_tax_item['tag_ids']})
            refund_repartition_line_ids.update({'use_in_tax_closing': refund_tax_item['use_in_tax_closing']})

            refund_line_det.append((0, credit_tax_pos, refund_repartition_line_ids))
            credit_tax_pos = credit_tax_pos + 1

        _logger.info("Service API : Invoce Lines (%s)",invoice_line_det)
        tax_vals.update({'refund_repartition_line_ids': refund_line_det})

        account_tax_id = self.env['account.tax'].create(tax_vals)
        #action = account_move_id.action_post()
        if account_tax_id:
            _logger.info("Service API : Tax Created (%s)",account_tax_id.id)
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'account_tax_id' : account_tax_id.id,

            })
