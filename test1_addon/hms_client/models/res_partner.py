import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class PartnerCreateAPI(models.Model):
    _name = 'partner.api.create'

    @api.model
    def action_create_partner(self, vals):

        event_type = ''
        partner_id = False
        partner_vals = {}

        if 'event_type' in vals:
            event_type = vals.get('event_type')

        if 'partner_id' in vals:
            partner_id = int(vals.get('partner_id'))

        if 'name' in vals:
            name = vals.get('name', False)
            partner_vals.update({'name': name or False})

        if 'company_type' in vals:
            type = vals.get('company_type', False)
            partner_vals.update({'company_type': type or False})

        if 'street' in vals:
            street = vals.get('street', False)
            partner_vals.update({'street': street or False})

        if 'street2' in vals:
            street2 = vals.get('street2', False)
            partner_vals.update({'street2': street2 or False})

        if 'city' in vals:
            city = vals.get('city', False)
            partner_vals.update({'city': city or False})

        if 'state_id' in vals:
            state = int(vals.get('state_id', False))
            partner_vals.update({'state_id': state or False})

        if 'zip' in vals:
            zip = vals.get('zip', False)
            partner_vals.update({'zip': zip or False})

        if 'country_id' in vals:
            country = int(vals.get('country_id', False))
            partner_vals.update({'country_id': country or False})

        if 'phone' in vals:
            phone = vals.get('phone', False)
            partner_vals.update({'phone': phone or False})

        if 'mobile' in vals:
            mobile = vals.get('mobile', False)
            partner_vals.update({'mobile': mobile or False})

        if 'email' in vals:
            email = vals.get('email', False)
            partner_vals.update({'email': email or False})

        if 'website' in vals:
            website = vals.get('website', False)
            partner_vals.update({'website': website or False})

        if 'vat' in vals:
            vat = vals.get('vat', False)
            partner_vals.update({'vat': vat or False})

        if 'gst_treatment' in vals:
            gst = vals.get('l10n_in_gst_treatment', False)
            partner_vals.update({'l10n_in_gst_treatment': gst or False})

        if 'property_account_receivable_id' in vals:
            property_account_receivable_id = int(vals.get('property_account_receivable_id', False))
            partner_vals.update({'property_account_receivable_id': property_account_receivable_id or False})

        if 'property_account_payable_id' in vals:
            property_account_payable_id = int(vals.get('property_account_payable_id', False))
            partner_vals.update({'property_account_payable_id': property_account_payable_id or False})

        # if 'operating_unit_id' in vals:
        #     operating_unit_id = int(vals.get('operating_unit_id', False))
        #     partner_vals.update({'operating_unit_id': operating_unit_id or False})

        if 'operating_unit_ids' in vals:
            operating_unit_ids = []
            operating_unit_string = vals['operating_unit_ids']
            _logger.info("Service API : operating_unit_ids %s", operating_unit_string)
            if operating_unit_string:
                operating_unit_list = operating_unit_string.split(',')
                for operating_unit_id in operating_unit_list:
                    operating_unit_ids.append(int(operating_unit_id))
                _logger.info("Service API : operating_unit_ids Id List %s", operating_unit_ids)
                partner_vals.update({'operating_unit_ids': [(6, 0, operating_unit_ids or [])]})

        # if 'company_id' in vals:
        #     company_id = (vals.get('company_id', False))
        #     partner_vals.update({'company_id': company_id or False})
        # else:
        #     _logger.info('Service API : Company ID Not Available Returning')
        #     status_code = 401
        #     return json.dumps({
        #         'status': 'REJECTED',
        #         'status_code': status_code,
        #         'msg': "An Error Occurred - Company ID Not Available",
        #     })

        if 'company_ids' in vals:
            company_ids = []
            company_string = vals['company_ids']
            _logger.info("Service API : Company String %s", company_string)
            if company_string:
                company_list = company_string.split(',')
                for company_id in company_list:
                    company_ids.append(int(company_id))
                _logger.info("Service API : Company Id List %s", company_ids)
                partner_vals.update({'company_ids': [(6, 0, company_ids or [])]})

        _logger.info("Service API : Partner Details %s %s", vals, self.env.user.company_id)
        # self.env.user.company_id = (vals['company_id'])
        _logger.info("Service API Event Type  : %s", event_type)
        if event_type == 'create':
            partner = self.env['res.partner'].create(partner_vals)
            if 'bank_details' in vals:
                bank_line = vals.get('bank_details')
                account_val = {}
                bank_val = {}
                bank_ifsc = self.env['res.bank'].search([('bic', '=', bank_line['bank_ifsc_code'])])
                if bank_ifsc:
                    account_val.update(
                        {'acc_number': bank_line['account_number'], 'partner_id': partner.id,
                         'bank_id': bank_ifsc.id})
                    bank_account = self.env['res.partner.bank'].create(account_val)
                else:
                    if bank_line['bank_ifsc_code']:
                        bank_val.update({'bic': bank_line['bank_ifsc_code']})

                    if bank_line['bank_name']:
                        bank_val.update({'name': bank_line['bank_name']})
                        if 'bank_street' in bank_line:
                            bank_val.update({'street': bank_line['bank_street']})
                        if 'bank_street2' in vals:
                            bank_val.update({'street2': bank_line['bank_street2']})
                        if 'bank_city' in bank_line:
                            bank_val.update({'city': bank_line['bank_city']})
                        if 'bank_state_id' in bank_line:
                            bank_val.update({'state': bank_line['bank_state_id']})
                        if 'bank_country_id' in bank_line:
                            bank_val.update({'country': bank_line['bank_country_id']})
                        if 'bank_phone' in bank_line:
                            bank_val.update({'phone': bank_line['bank_phone']})
                        if 'bank_zip' in bank_line:
                            bank_val.update({'zip': bank_line['bank_zip']})
                        if 'bank_email' in bank_line:
                            bank_val.update({'email': bank_line['bank_email']})

                        bank_id = self.env['res.bank'].create(bank_val)
                        account_val.update(
                            {'acc_number': bank_line['account_number'], 'partner_id': partner.id,
                             'acc_type': bank_line['type'],
                             'acc_holder_name': bank_line['account_holder_name'], 'bank_id': bank_id.id})
                    bank_account = self.env['res.partner.bank'].create(account_val)

            if partner:
                _logger.info("Service API : Partner Created")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'partner_id': partner.id,
                })
        elif event_type == 'update':
            if not partner_id:
                status_code = 401
                return json.dumps({
                    'status': 'REJECTED',
                    'status_code': status_code,
                    'msg': "An Error Occurred - Partner ID Not Available",
                })
            partner_obj = self.env['res.partner'].search([('id', '=', partner_id)])
            partner_obj.update(partner_vals)
            _logger.info("Service API : Partner Updated")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'partner_id': partner_id,
            })
        status_code = 401
        _logger.info("Service API : An Error Occurred - Event Type Not Available")
        return json.dumps({
            'status': 'REJECTED',
            'status_code': status_code,
            'msg': "An Error Occurred - Event Type Not Available",
        })


class PartnerSearchAPI(models.Model):
    _name = 'partner.api.search'

    @api.model
    def action_search_partner(self, vals):
        partner = self.env['res.partner'].browse(vals['partner_id'])
        if partner:
            _logger.info("Service API : Partner Verified")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'partner_id': partner.id,
                # 'dbname': self._cr.dbname,

            })
