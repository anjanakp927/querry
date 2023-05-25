# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    quotation_id = fields.Many2one('purchase.quotation', string='Purchase Quotation')
    name = fields.Char()
    amount_total_currency = fields.Monetary(string='Total(Company Currency)', store=True, readonly=True,
                                            compute='_amount_all', tracking=4)
    company_currency_id = fields.Many2one(related='company_id.currency_id', string='Company Currency',
                                          readonly=True, store=True,
                                          help='Utility field to express amount currency')
    hms_purchase_mode = fields.Selection([('cash', 'Cash'), ('credit', 'Credit')], string="Purchase Mode")
    # added by me
    @api.model
    def create(self, vals):
        # if self.state=='draft':
        #     vals["name"]='New'
        result = super(PurchaseOrder, self).create(vals)
        if result.state == 'draft':
            result.name = 'New'

        # result.state = 'purchase'
        # result.button_confirm()
        return result

    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        self.name = self.env['ir.sequence'].next_by_code('purchase.order')
        return result

    def action_cancel(self):
        for purchase_order in self:
            if purchase_order.state == 'purchase':
                if any(move.state == 'posted' for move in purchase_order.invoice_ids):
                    raise UserError(_('You cannot cancel a purchase order if invoice has been set to \'Posted\'.'))
        return super(PurchaseOrder, self).action_cancel()

    @api.depends('order_line.price_total', 'currency_id')
    def _amount_all(self):
        super(PurchaseOrder, self)._amount_all()
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            amount_currency = order.currency_id._convert(amount_untaxed + amount_tax, order.company_id.currency_id,
                                                         order.company_id, order.date_order)
            order.update({
                'amount_total_currency': amount_currency,
            })



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    company_currency_id = fields.Many2one(related='company_id.currency_id', string='Company Currency',
                                          readonly=True, store=True,
                                          help='Utility field to express amount currency')

    price_subtotal_currency = fields.Monetary(compute='_compute_amount', string='Subtotal(Company Currency)',
                                              readonly=True,
                                              store=True)
    price_total_currency = fields.Monetary(compute='_compute_amount', string='Total(Company Currency)', readonly=True,
                                           store=True)

    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        super(PurchaseOrderLine, self)._compute_amount()
        # for line in self:
        #     price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        #     taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
        #                                     product=line.product_id, partner=line.order_id.partner_shipping_id)
        #     if line.order_id.currency_id:
        #         price_total_currency = line.order_id.currency_id._convert(taxes['total_included'],
        #                                                                   line.order_id.company_id.currency_id,
        #                                                                   line.order_id.company_id, line.order_id.date_order)
        #         price_subtotal_currency = line.order_id.currency_id._convert(taxes['total_excluded'],
        #                                                                      line.order_id.company_id.currency_id,
        #                                                                      line.order_id.company_id, line.order_id.date_order)
        #         line.update({
        #             'price_total_currency': price_total_currency,
        #             'price_subtotal_currency': price_subtotal_currency,
        #         })
