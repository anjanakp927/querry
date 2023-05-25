import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime


_logger = logging.getLogger(__name__)


class ProductCreateAPI(models.Model):
    _name = 'product.api.create'

    def create_product(self, values):
        _logger.info("Service API : Attempting to Create Product From Model")

        hsn_sac_master = False
        hsn_sac_code = False
        if 'l10n_in_hsn_code_master' in values:
            l10n_in_hsn_code = values.get('l10n_in_hsn_code_master', False)
            _logger.info("Service API : Checking HSN Code (%s)", l10n_in_hsn_code)
            hsn_sac_code = self.env['hsn.sac.master'].search([('l10n_in_hsn_code', '=', str(l10n_in_hsn_code))],
                                                             limit=1)
        if not hsn_sac_code:
            _logger.info("Service API : HSN Code not available Attempting to create HSN")
            hsn_sac_master = {'l10n_in_hsn_code': values.get('l10n_in_hsn_code_master', False)}
        if hsn_sac_master:
            hsn_sac_code = self.env['hsn.sac.master'].create(hsn_sac_master)

        if hsn_sac_code:
            values.update({'l10n_in_hsn_code_master': hsn_sac_code.id or False})
        else:
            _logger.info("Service API : Unable to create HSN Code Assigning default ID - 1")
            #This is not logical need to correct
            values.update({'l10n_in_hsn_code_master': int("1") or False})

        if 'operating_unit_ids' in values:
            operating_unit_ids = []
            operating_unit_string = values['operating_unit_ids']
            _logger.info("Service API : operating_unit_ids %s", operating_unit_string)
            if operating_unit_string:
                operating_unit_list = operating_unit_string.split(',')
                for operating_unit_id in operating_unit_list:
                    operating_unit_ids.append(int(operating_unit_id))
                _logger.info("Service API : operating_unit_ids Id List %s", operating_unit_ids)
                values.update({'operating_unit_ids': [(6, 0, operating_unit_ids or [])]})

        if 'taxes_id' in values:
            tax_ids = []
            tax_string = values['taxes_id']
            _logger.info("Service API : Taxes String %s", tax_string)
            if tax_string:
                tax_list = tax_string.split(',')
                for tax_id in tax_list:
                    tax_ids.append(int(tax_id))
                _logger.info("Service API : Tax Id List %s", tax_ids)
                values.update({'taxes_id': [(6, 0, tax_ids or [])]})

        if 'company_ids' in values:
            company_ids = []
            company_string = values['company_ids']
            _logger.info("Service API : Company String %s", company_string)
            if company_string:
                company_list = company_string.split(',')
                for company_id in company_list:
                    company_ids.append(int(company_id))
                _logger.info("Service API : Company Id List %s", company_ids)
                values.update({'company_ids': [(6, 0, company_ids or [])]})

        product_id = self.env['product.product'].create(values)

        if product_id:
            _logger.info("Service API : Product Created %s",product_id.id)
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'product_id': product_id.id,

            })

    @api.model
    def action_create_product(self, vals):
        return self.create_product(vals)


class ProductSearchAPI(models.Model):
    _name = 'product.api.search'

    @api.model
    def action_search_product(self, vals):
        product_id = self.env['product.template'].browse(vals['product_id'])
        if product_id:
            _logger.info("Service API : Product Verified")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'product_id': product_id.id,

            })
