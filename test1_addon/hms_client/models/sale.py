import json
import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderCreateAPI(models.Model):
    _name = 'sale.order.api.create'

    @api.model
    def action_sale_order_create(self, params):

        sale_order_vals = {}

        if 'partner_id' in params:
            partner_id = int(params.get('partner_id'))
            sale_order_vals.update({'partner_id': partner_id or False})

        if 'l10n_in_gst_treatment' in params:
            l10n_in_gst_treatment = (params.get('l10n_in_gst_treatment'))
            sale_order_vals.update({'l10n_in_gst_treatment': l10n_in_gst_treatment or False})

        if 'validity_date' in params:
            validity_date = (params.get('validity_date'))
            sale_order_vals.update({'validity_date': validity_date or False})

        if 'date_order' in params:
            date_order = (params.get('date_order'))
            sale_order_vals.update({'date_order': date_order or False})

        if 'payment_term_id' in params:
            payment_term_id = int(params.get('payment_term_id', False))
            sale_order_vals.update({'payment_term_id': payment_term_id or False})

        if 'salesperson' in params:
            salesperson = int(params.get('salesperson', False))
            sale_order_vals.update({'user_id': salesperson or False})

        if 'fiscal_position_id' in params:
            fiscal_position_id = int(params.get('fiscal_position_id', False))
            sale_order_vals.update({'fiscal_position_id': fiscal_position_id or False})

        if 'l10n_in_journal_id' in params:
            l10n_in_journal_id = int(params.get('l10n_in_journal_id', False))
            sale_order_vals.update({'l10n_in_journal_id': l10n_in_journal_id or False})

        if 'company_id' in params:
            company_id = int(params.get('company_id', False))
            sale_order_vals.update({'company_id': company_id or False})

        if 'operating_unit_id' in params:
            operating_unit_id = int(params.get('operating_unit_id', False))
            sale_order_vals.update({'operating_unit_id': operating_unit_id or False})

        if 'client_order_ref' in params:
            client_order_ref = (params.get('client_order_ref', False))
            sale_order_vals.update({'client_order_ref': client_order_ref or False})

        if 'picking_policy' in params:
            picking_policy = (params.get('picking_policy', False))
            sale_order_vals.update({'picking_policy': picking_policy or False})

        if 'warehouse_id' in params:
            warehouse_id = (params.get('warehouse_id', False))
            sale_order_vals.update({'warehouse_id': warehouse_id or False})

        if 'order_lines' in params:
            order_lines = params.get('order_lines')
            _logger.info("Service API : Sale Order Details (%s)")
            sale_order_pos = 0
            sale_order_line_det = []

            for sale_order_item in order_lines:
                sale_order_line_items = {}

                sale_order_line_items.update({'product_id': int(sale_order_item['product_id'])})
                sale_order_line_items.update({'name': str(sale_order_item['description'])})
                sale_order_line_items.update({'product_uom_qty': float(sale_order_item['product_qty'])})
                sale_order_line_items.update({'product_uom': int(sale_order_item['product_uom'])})
                sale_order_line_items.update({'price_unit': float(sale_order_item['price_unit'])})
                if 'taxes_id' in sale_order_item:
                    tax_ids = []
                    tax_string = sale_order_item['taxes_id']
                    _logger.info("Service API : Taxes String %s", tax_string)
                    if tax_string:
                        tax_list = tax_string.split(',')
                        for tax_id in tax_list:
                            tax_ids.append(int(tax_id))
                        _logger.info("Service API : Tax Id List %s", tax_ids)
                        sale_order_line_items.update({'tax_id': [(6, 0, tax_ids or [])]})
                sale_order_line_det.append((0, sale_order_pos, sale_order_line_items))
                sale_order_pos = sale_order_pos + 1
            _logger.info("Service API :Sale Lines Details (%s)", sale_order_line_det)
            sale_order_vals.update({"order_line": sale_order_line_det})

        if 'event_type' in params:
            event_type = (params.get('event_type'))
            if event_type == 'create':
                sale_orderid = self.env['sale.order'].create(sale_order_vals)
                if sale_orderid:
                    sale_orderid.action_confirm()
                    _logger.info("Service API : Sale Order Created")
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'sale_order_id': sale_orderid.id,
                        'delivery_id': sale_orderid.picking_ids.id,

                    })
            if event_type == 'cancel':
                if 'sale_order_id' in params:
                    sale_order_id = int(params.get('sale_order_id'))
                    sale_order = self.env['sale.order'].browse(sale_order_id)
                    if sale_order.picking_ids.state != 'done':
                        sale_order.action_cancel()
                        _logger.info("Service API : Sale Order Cancelled (%s )", sale_order.id)
                        status = 'SUCCESS'
                        status_code = 200
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'sale_order_id': sale_order.id,
                            'delivery_id': 0,

                        })
                    else:
                        _logger.info("Service API : Sale Order cannot Cancelled Delivery has been created (%s )", sale_order.id)
                        status = 'FAILED'
                        status_code = 400
                        return json.dumps({
                            'status': status,
                            'status_code': status_code,
                            'sale_order_id': sale_order.id,
                            'delivery_id': 0,

                        })