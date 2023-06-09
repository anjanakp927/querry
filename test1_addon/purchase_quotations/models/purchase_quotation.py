# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang


class PurchaseQuotation(models.Model):
    _name = "purchase.quotation"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = "Purchase Quotation"
    _order = 'date_quotation desc, id desc'

    @api.depends('quotation_line.price_total')
    def _amount_all(self):
        for quotation in self:
            amount_untaxed = amount_tax = 0.0
            for line in quotation.quotation_line:
                line._compute_amount()
                amount_untaxed += line.price_subtotal

                amount_tax += line.price_tax
            quotation.update({
                'amount_untaxed': quotation.currency_id.round(amount_untaxed),
                'amount_tax': quotation.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.depends('state', 'quotation_line.qty_invoiced', 'quotation_line.qty_received', 'quotation_line.product_qty')
    def _get_invoiced(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for quotation in self:
            if quotation.state not in ('purchase', 'done'):
                quotation.invoice_status = 'no'
                continue
            if any(
                    float_compare(
                        line.qty_invoiced,
                        line.product_qty if line.product_id.purchase_method == 'purchase' else line.qty_received,
                        precision_digits=precision,)
                    == -1
                    for line in quotation.quotation_line.filtered(lambda l: not l.display_type)
            ):
                quotation.invoice_status = 'to invoice'
            elif (
                    all(
                        float_compare(
                            line.qty_invoiced,
                            line.product_qty if line.product_id.purchase_method == "purchase" else line.qty_received,
                            precision_digits=precision,
                        )
                        >= 0
                        for line in quotation.quotation_line.filtered(lambda l: not l.display_type)
                    )
                    and quotation.invoice_ids
            ):
                quotation.invoice_status = 'invoiced'
            else:
                quotation.invoice_status = 'no'

    @api.depends('quotation_line.invoice_lines.move_id')
    def _compute_invoice(self):
        for quotation in self:
            invoices = quotation.mapped('quotation_line.invoice_lines.move_id')
            quotation.invoice_ids = invoices
            quotation.invoice_count = len(invoices)

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    name = fields.Char('Quotation Reference', index=True, copy=False, default='New')
    origin = fields.Char('Source Document', copy=False,
                         help="Reference of the document that generated this purchase quotation "
                              "request (e.g. a sales quotation)")
    partner_ref = fields.Char('Vendor Reference', copy=False,
                              help="Reference of the sales quotation or bid sent by the vendor. "
                                   "It's used to do the matching when you receive the "
                                   "products as this reference is usually written on the "
                                   "delivery quotation sent by your vendor.")
    date_quotation = fields.Datetime('Quotation Date', required=True, states=READONLY_STATES, index=True, copy=False,
                                     default=fields.Datetime.now, \
                                     help="Depicts the date where the Quotation should be validated and converted into a purchase quotation.")
    date_approve = fields.Datetime('Confirmation Date', readonly=1, index=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES,
                                 change_default=True, tracking=True,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    dest_address_id = fields.Many2one('res.partner',
                                      domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                      string='Drop Ship Address', states=READONLY_STATES,
                                      help="Put an address if you want to deliver directly from the vendor to the customer. "
                                           "Otherwise, keep empty to deliver to your own company.")
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES,
                                  default=lambda self: self.env.company.currency_id.id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Quotation'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    quotation_line = fields.One2many('purchase.quotation.line', 'quotation_id', string='Quotation Lines',
                                     states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    notes = fields.Text('Terms and Conditions')

    invoice_count = fields.Integer(compute="_compute_invoice", string='Bill Count', copy=False, default=0, store=True)
    invoice_ids = fields.Many2many('account.move', compute="_compute_invoice", string='Bills', copy=False, store=True)
    invoice_status = fields.Selection([
        ('no', 'Nothing to Bill'),
        ('to invoice', 'Waiting Bills'),
        ('invoiced', 'Fully Billed'),
    ], string='Billing Status', compute='_get_invoiced', store=True, readonly=True, copy=False, default='no')

    # There is no inverse function on purpose since the date may be different on each line
    date_planned = fields.Datetime(string='Receipt Date', index=True)

    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     tracking=True)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')

    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position',
                                         domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    payment_term_id = fields.Many2one('account.payment.term', 'Payment Terms',
                                      domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    incoterm_id = fields.Many2one('account.incoterms', 'Incoterm', states={'done': [('readonly', True)]},
                                  help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")

    product_id = fields.Many2one('product.product', related='quotation_line.product_id', string='Product',
                                 readonly=False)
    user_id = fields.Many2one(
        'res.users', string='Purchase Representative', index=True, tracking=True,
        default=lambda self: self.env.user, check_company=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES,
                                 default=lambda self: self.env.company.id)
    currency_rate = fields.Float("Currency Rate", compute='_compute_currency_rate', compute_sudo=True, store=True,
                                 readonly=True,
                                 help='Ratio between the purchase quotation currency and the company currency')

    purchase_order_ids = fields.One2many('purchase.order', 'quotation_id', string='Purchase Orders')
    purchase_order_count = fields.Integer(string='Sale Orders', compute='_compute_purchase_order_count')
    revision_ids = fields.One2many('purchase.quotation.revision', 'quotation_id', string='Revisions')
    revision_count = fields.Integer(string='Revisions', compute='_compute_revision_count')
    quotation_id = fields.Many2one('purchase.quotation', string='Purchase Quotation')
    number = fields.Integer(string='Revisions Number', default=1)
    type = fields.Selection([
        ('normal', 'Quotation'),
        ('revise', 'Revise Quotation'),
    ], string='Status', copy=False, index=True, default='normal')

    last_purchase_ids = fields.One2many('last.five.purchase', 'last_purchase_id', string='Last Purchase')
    stock_details_id = fields.One2many('show.stock.details', 'stock_details_ids', string='Last Purchase')

    @api.onchange('quotation_line')
    def onchange_quotation_lines(self):
        if self.quotation_line:
            list = [(5, 0)]
            list1 = [(5, 0)]
            for rec in self.quotation_line:
                purchase_lines = self.env['purchase.order.line'].sudo().search(
                    [('product_id', '=', rec.product_id.id)
                     ], order='create_date desc', limit=5)
                quant_ids = self.env['stock.quant'].sudo().search(
                    [('product_id', '=', rec.product_id.id), ('location_id.usage', '=', 'internal')])
                for i in purchase_lines:
                    list.append((0, 0, {
                        'product_id': i.product_id,
                        'vendor_id': i.partner_id,
                        'price': i.price_total,
                        'product_qty': i.product_qty,
                        'date_planned': i.date_planned,
                    }))
                for i in quant_ids:
                    list1.append((0, 0, {
                        'location_id': i.location_id,
                        'available_quantity': i.available_quantity,
                        'quantity': i.quantity,
                        'company_id': i.company_id,
                    }))
            self.last_purchase_ids = list
            self.stock_details_id = list1

    @api.depends('purchase_order_ids')
    def _compute_purchase_order_count(self):
        for order in self:
            order.purchase_order_count = len(order.purchase_order_ids)

    def action_view_purchase_order(self):
        action = self.env.ref('purchase.purchase_form_action').read()[0]
        action['domain'] = [('id', 'in', self.mapped('purchase_order_ids.id')), ]
        orders = self.mapped('purchase_order_ids')
        if len(orders) == 1:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = orders.id
        return action

    @api.depends('revision_ids')
    def _compute_revision_count(self):
        for order in self:
            order.revision_count = self.env['purchase.quotation'].search_count([('origin', '=', self.name)])

    # disabled by me
    def action_view_revisions(self):
        action = self.env.ref('purchase_quotations.action_revisions').read()[0]
        revisions = self.env['purchase.quotation'].search([('origin', '=', self.name)])
        action['domain'] = [('id', 'in', revisions.ids)]
        action['name'] = 'Quotation Revision'
        if len(revisions.ids) == 1:
            action['views'] = [(self.env.ref('purchase_quotations.purchase_quotation_form').id, 'form')]
            action['res_id'] = revisions.id
        return action

    # def action_revise_quotation(self):
    #     revise_quotation = self.env['purchase.quotation'].create({
    #         'partner_id': self.partner_id.id,
    #         'quotation_id': self.id,
    #         'state': 'draft',
    #         'origin': self.name,
    #         'type': 'revise',
    #         'number': self.number,
    #         'date_quotation': fields.Datetime.now()
    #     })
    #     for line in self.quotation_line:
    #         self.env['purchase.quotation.line'].create({
    #             'quotation_id': revise_quotation.id,
    #             'product_id': line.product_id.id,
    #             'name': line.product_id.display_name,
    #             'product_qty': line.product_uom_qty,
    #             'product_uom': line.product_uom.id,
    #             'display_type': line.display_type,
    #             'price_unit': line.price_unit,
    #             'date_planned': line.date_planned,
    #             'taxes_id': [(6, 0, line.taxes_id.ids)],
    #
    #         })
    #     self.number += 1
    #     # self.write({
    #     #     'revision_ids': [(4, revise_quotation.id)],
    #     # })

    @api.constrains('company_id', 'quotation_line')
    def _check_quotation_line_company_id(self):
        for quotation in self:
            companies = quotation.quotation_line.product_id.company_id
            if companies and companies != quotation.company_id:
                bad_products = quotation.quotation_line.product_id.filtered(
                    lambda p: p.company_id and p.company_id != quotation.company_id)
                raise ValidationError((
                        _("Your quotation contains products from company %s whereas your quotation belongs to company %s. \n Please change the company of your quotation or remove the products from other companies (%s).") % (
                    ', '.join(companies.mapped('display_name')),
                    quotation.company_id.display_name,
                    ', '.join(bad_products.mapped('display_name')))))

    def _compute_access_url(self):
        super(PurchaseQuotation, self)._compute_access_url()
        for quotation in self:
            quotation.access_url = '/my/purchase/%s' % (quotation.id)

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = args or []
    #     domain = []
    #     if name:
    #         domain = ['|', ('name', operator, name), ('partner_ref', operator, name)]
    #     purchase_quotation_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
    #     return models.lazy_name_get(self.browse(purchase_quotation_ids).with_user(name_get_uid))

    @api.depends('date_quotation', 'currency_id', 'company_id', 'company_id.currency_id')
    def _compute_currency_rate(self):
        for quotation in self:
            quotation.currency_rate = self.env['res.currency']._get_conversion_rate(quotation.company_id.currency_id,
                                                                                    quotation.currency_id,
                                                                                    quotation.company_id,
                                                                                    quotation.date_quotation)

    @api.depends('name', 'partner_ref')
    def name_get(self):
        result = []
        for po in self:
            name = po.name
            if po.partner_ref:
                name += ' (' + po.partner_ref + ')'
            if self.env.context.get('show_total_amount') and po.amount_total:
                name += ': ' + formatLang(self.env, po.amount_total, currency_obj=po.currency_id)
            result.append((po.id, name))
        return result

    # @api.model
    # def create(self, vals):
    #     company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
    #     self_comp = self.with_company(company_id)
    #     if vals.get('name', 'New') == 'New':
    #         seq_date = None
    #         if 'date_quotation' in vals:
    #             seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_quotation']))
    #         vals['name'] = self_comp.env['ir.sequence'].next_by_code('purchase.quotation',
    #                                                                  sequence_date=seq_date) or '/'
    #     return super(PurchaseQuotation, self.with_context(company_id=company_id)).create(vals)

    def write(self, vals):
        res = super(PurchaseQuotation, self).write(vals)
        if vals.get('date_planned'):
            self.quotation_line.filtered(lambda line: not line.display_type).date_planned = vals['date_planned']
        return res

    def unlink(self):
        for quotation in self:
            if not quotation.state == 'cancel':
                raise UserError(_('In quotation to delete a purchase quotation, you must cancel it first.'))
        return super(PurchaseQuotation, self).unlink()

    def copy(self, default=None):
        ctx = dict(self.env.context)
        ctx.pop('default_product_id', None)
        self = self.with_context(ctx)
        new_po = super(PurchaseQuotation, self).copy(default=default)
        for line in new_po.quotation_line:
            if new_po.date_planned and not line.display_type:
                line.date_planned = new_po.date_planned
            elif line.product_id:
                seller = line.product_id._select_seller(
                    partner_id=line.partner_id, quantity=line.product_qty,
                    date=line.quotation_id.date_quotation and line.quotation_id.date_quotation.date(),
                    uom_id=line.product_uom)
                line.date_planned = line._get_date_planned(seller)
        return new_po

    # def _track_subtype(self, init_values):
    #     self.ensure_one()
    #     if 'state' in init_values and self.state == 'purchase':
    #         return self.env.ref('purchase.mt_rfq_approved')
    #     elif 'state' in init_values and self.state == 'to approve':
    #         return self.env.ref('purchase.mt_rfq_confirmed')
    #     elif 'state' in init_values and self.state == 'done':
    #         return self.env.ref('purchase.mt_rfq_done')
    #     return super(PurchaseQuotation, self)._track_subtype(init_values)

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        # Ensures all properties and fiscal positions
        # are taken with the company of the quotation
        # if not defined, with_company doesn't change anything.
        self = self.with_company(self.company_id)
        if not self.partner_id:
            self.fiscal_position_id = False
            self.currency_id = self.env.company.currency_id.id
        else:
            self.fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id)
            self.payment_term_id = self.partner_id.property_supplier_payment_term_id.id
            self.currency_id = self.partner_id.property_purchase_currency_id.id or self.env.company.currency_id.id
        return {}

    @api.onchange('fiscal_position_id')
    def _compute_tax_id(self):
        """
        Trigger the recompute of the taxes if the fiscal position is changed on the PO.
        """
        for quotation in self:
            quotation.quotation_line._compute_tax_id()

    @api.onchange('partner_id')
    def onchange_partner_id_warning(self):
        if not self.partner_id or not self.env.user.has_group('purchase.group_warning_purchase'):
            return
        warning = {}
        title = False
        message = False

        partner = self.partner_id

        # If partner has no warning, check its company
        if partner.purchase_warn == 'no-message' and partner.parent_id:
            partner = partner.parent_id

        if partner.purchase_warn and partner.purchase_warn != 'no-message':
            # Block if partner only has warning but parent company is blocked
            if partner.purchase_warn != 'block' and partner.parent_id and partner.parent_id.purchase_warn == 'block':
                partner = partner.parent_id
            title = _("Warning for %s") % partner.name
            message = partner.purchase_warn_msg
            warning = {
                'title': title,
                'message': message
            }
            if partner.purchase_warn == 'block':
                self.update({'partner_id': False})
            return {'warning': warning}
        return {}

    def action_rfq_send(self):
        '''
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        '''
        # self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            if self.env.context.get('send_rfq', False):
                template_id = ir_model_data.get_object_reference('purchase', 'email_template_edi_purchase')[1]
            else:
                template_id = ir_model_data.get_object_reference('purchase', 'email_template_edi_purchase_done')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchase.quotation',
            'active_model': 'purchase.quotation',
            'active_id': self.ids[0],
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'mark_rfq_as_sent': True,
        })

        # In the case of a RFQ or a PO, we want the "View..." button in line with the state of the
        # object. Therefore, we pass the model description in the context, in the language in which
        # the template is rendered.
        lang = self.env.context.get('lang')
        if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
            template = self.env['mail.template'].browse(ctx['default_template_id'])
            if template and template.lang:
                lang = template._render_template(template.lang, ctx['default_model'], ctx['default_res_id'])

        self = self.with_context(lang=lang)
        if self.state in ['draft', 'sent']:
            ctx['model_description'] = _('Request for Quotation')
        else:
            ctx['model_description'] = _('Purchase Quotation')

        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_rfq_as_sent'):
            self.filtered(lambda o: o.state == 'draft').write({'state': 'sent'})
        return super(PurchaseQuotation, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)

    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env.ref('purchase.report_purchase_quotation').report_action(self)

    # def button_approve(self, force=False):
    #     self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
    #     self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
    #     return {}

    def button_draft(self):
        self.write({'state': 'draft'})
        return {}

    def confirmation(self):
        # company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        # self_comp = self.with_company(company_id)
        # if vals.get('name', 'New') == 'New':
        #     print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
        #     seq_date = None
        #     if 'date_quotation' in vals:
        #         seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_quotation']))
        #     vals['name'] = self_comp.env['ir.sequence'].next_by_code('purchase.quotation',
        #                                                              sequence_date=seq_date) or '/'
        # return super(PurchaseQuotation, self.with_context(company_id=company_id)).create(vals)
        self.name = self.env["ir.sequence"].next_by_code("purchase.quotation")
        self.write({'state': 'confirmed'})

    def button_confirm(self):
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.partner_id.id,
            'quotation_id': self.id,
            'origin': self.name,
            'date_order': fields.Datetime.now()
        })
        for line in self.quotation_line:
            self.env['purchase.order.line'].create({
                'order_id': purchase_order.id,
                'product_id': line.product_id.id,
                'name': line.product_id.display_name,
                'product_qty': line.product_qty,
                'product_uom': line.product_uom.id,
                'display_type': line.display_type,
                'price_unit': line.price_unit,
                'date_planned': line.date_planned,
                'taxes_id': [(6, 0, line.taxes_id.ids)],
            })
        self.write({
            'purchase_order_ids': [(4, purchase_order.id)],
            'state': 'purchase',
            # 'date_order': fields.Datetime.now()
        })
        return purchase_order

    # disabled by me

    # def button_confirm(self):
    # purchase_order = self.env['purchase.order'].create({
    #     'partner_id': self.partner_id.id,
    #     'quotation_id': self.id,
    #     'state': 'purchase',
    #     'origin': self.name,
    #     'date_order': fields.Datetime.now()
    # })
    # for line in self.quotation_line:
    #     self.env['purchase.order.line'].create({
    #         'order_id': purchase_order.id,
    #         'product_id': line.product_id.id,
    #         'name': line.product_id.display_name,
    #         'product_qty': line.product_qty,
    #         'product_uom': line.product_uom.id,
    #         'display_type': line.display_type,
    #         'price_unit': line.price_unit,
    #         'date_planned': line.date_planned,
    #         'taxes_id': [(6, 0, line.taxes_id.ids)],
    #     })
    # self.write({
    #     'purchase_order_ids': [(4, purchase_order.id)],
    #     'state': 'purchase',
    #     # 'date_order': fields.Datetime.now()
    # })
    # purchase_order.button_confirm()
    # view = self.env.ref('purchase.purchase_form_action')
    # action = self.env.ref('purchase.purchase_form_action').read()[0]
    # action['domain'] = [('id', 'in', self.mapped('purchase_order_ids.id'))]
    # orders = self.mapped('purchase_order_ids')
    # if len(orders) == 1:
    #     action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
    #     action['res_id'] = orders.id
    # return action

    def button_cancel(self):
        for quotation in self:
            for inv in quotation.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(
                        _("Unable to cancel this purchase quotation. You must first cancel the related vendor bills."))

        self.write({'state': 'cancel'})

    def button_unlock(self):
        self.write({'state': 'purchase'})

    def button_done(self):
        self.write({'state': 'done'})

    def _add_supplier_to_product(self):
        # Add the partner in the supplier list of the product if the supplier is not registered for
        # this product. We limit to 10 the number of suppliers for a product to avoid the mess that
        # could be caused for some generic products ("Miscellaneous").
        for line in self.quotation_line:
            # Do not add a contact as a supplier
            partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
            if line.product_id and partner not in line.product_id.seller_ids.mapped('name') and len(
                    line.product_id.seller_ids) <= 10:
                # Convert the price in the right currency.
                currency = partner.property_purchase_currency_id or self.env.company.currency_id
                price = self.currency_id._convert(line.price_unit, currency, line.company_id,
                                                  line.date_quotation or fields.Date.today(), round=False)
                # Compute the price for the template's UoM, because the supplier's UoM is related to that UoM.
                if line.product_id.product_tmpl_id.uom_po_id != line.product_uom:
                    default_uom = line.product_id.product_tmpl_id.uom_po_id
                    price = line.product_uom._compute_price(price, default_uom)

                supplierinfo = {
                    'name': partner.id,
                    'sequence': max(
                        line.product_id.seller_ids.mapped('sequence')) + 1 if line.product_id.seller_ids else 1,
                    'min_qty': 0.0,
                    'price': price,
                    'currency_id': currency.id,
                    'delay': 0,
                }
                # In case the quotation partner is a contact address, a new supplierinfo is created on
                # the parent company. In this case, we keep the product name and code.
                seller = line.product_id._select_seller(
                    partner_id=line.partner_id,
                    quantity=line.product_qty,
                    date=line.quotation_id.date_quotation and line.quotation_id.date_quotation.date(),
                    uom_id=line.product_uom)
                if seller:
                    supplierinfo['product_name'] = seller.product_name
                    supplierinfo['product_code'] = seller.product_code
                vals = {
                    'seller_ids': [(0, 0, supplierinfo)],
                }
                try:
                    line.product_id.write(vals)
                except AccessError:  # no write access rights -> just ignore
                    break

    #                 disabled by me

    # def action_view_invoice(self):
    #     '''
    #     This function returns an action that display existing vendor bills of given purchase quotation ids.
    #     When only one found, show the vendor bill immediately.
    #     '''
    #     action = self.env.ref('account.action_move_in_invoice_type')
    #     result = action.read()[0]
    #     create_bill = self.env.context.get('create_bill', False)
    #     # override the context to get rid of the default filtering
    #     result['context'] = {
    #         'default_type': 'in_invoice',
    #         'default_company_id': self.company_id.id,
    #         'default_purchase_id': self.id,
    #         'default_partner_id': self.partner_id.id,
    #     }
    #     # Invoice_ids may be filtered depending on the user. To ensure we get all
    #     # invoices related to the purchase quotation, we read them in sudo to fill the
    #     # cache.
    #     self.sudo()._read(['invoice_ids'])
    #     # choose the view_mode accordingly
    #     if len(self.invoice_ids) > 1 and not create_bill:
    #         result['domain'] = "[('id', 'in', " + str(self.invoice_ids.ids) + ")]"
    #     else:
    #         res = self.env.ref('account.view_move_form', False)
    #         form_view = [(res and res.id or False, 'form')]
    #         if 'views' in result:
    #             result['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
    #         else:
    #             result['views'] = form_view
    #         # Do not set an invoice_id if we want to create a new bill.
    #         if not create_bill:
    #             result['res_id'] = self.invoice_ids.id or False
    #     result['context']['default_invoice_origin'] = self.name
    #     result['context']['default_ref'] = self.partner_ref
    #     return result

    # @api.onchange("quotation_line")
    # def _onchange_product_id(self):
    #
    #     list = []
    #     self._cr.execute('''select product_id,price_unit from purchase_order where (product_id='%s')''' % (self.product_id))
    #     product_id = self._cr.fetchall()
    #     for id in product_id:
    #         list.append(id[0])
    #
    #     print(list,"++++++++++++++++++++++++++++++++++++++++++++++++++")
    #     #     for element in main_list:
    #     #         val = {"code": self.code,
    #     #                "name": self.account_name,
    #     #                "user_type_id": self.user_type_id.id,
    #     #                "company_id": element,
    #     #                'reconcile': True}
    #     #         self.env['account.account'].create(val)
    #     # else:
    #     #     raise ValidationError("The code of the account must be unique per company !")
    #
    #     # for rec in self:
    #     #     lines = []
    #     #     for lines in self.quotation_line:
    #     #         vals = {
    #     #             "product_id": lines.id,
    #     #         }
    #     #         lines.append((0, 0, vals))
    #     #         rec.last_purchase = lines


class PurchaseQuotationLine(models.Model):
    _name = 'purchase.quotation.line'
    _description = 'Purchase Quotation Line'
    _order = 'quotation_id, sequence, id'

    name = fields.Text(string='Description', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True)
    product_uom_qty = fields.Float(string='Total Quantity', compute='_compute_product_uom_qty', store=True)
    date_planned = fields.Datetime(string='Scheduled Date', index=True)
    taxes_id = fields.Many2many('account.tax', string='Taxes',
                                domain=['|', ('active', '=', False), ('active', '=', True)])
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',
                                  domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)],
                                 change_default=True)
    product_type = fields.Selection(related='product_id.type', readonly=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

    quotation_id = fields.Many2one('purchase.quotation', string='Quotation Reference', index=True, required=True,
                                   ondelete='cascade')
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    company_id = fields.Many2one('res.company', related='quotation_id.company_id', string='Company', store=True,
                                 readonly=True)
    state = fields.Selection(related='quotation_id.state', store=True, readonly=False)

    invoice_lines = fields.One2many('account.move.line', 'purchase_line_id', string="Bill Lines", readonly=True,
                                    copy=False)

    # Replace by invoiced Qty
    qty_invoiced = fields.Float(compute='_compute_qty_invoiced', string="Billed Qty", digits='Product Unit of Measure',
                                store=True)

    qty_received_method = fields.Selection([('manual', 'Manual')], string="Received Qty Method",
                                           compute='_compute_qty_received_method', store=True,
                                           help="According to product configuration, the recieved quantity can be automatically computed by mechanism :\n"
                                                "  - Manual: the quantity is set manually on the line\n"
                                                "  - Stock Moves: the quantity comes from confirmed pickings\n")
    qty_received = fields.Float("Received Qty", compute='_compute_qty_received', inverse='_inverse_qty_received',
                                compute_sudo=True, store=True, digits='Product Unit of Measure')
    qty_received_manual = fields.Float("Manual Received Qty", digits='Product Unit of Measure', copy=False)

    partner_id = fields.Many2one('res.partner', related='quotation_id.partner_id', string='Partner', readonly=True,
                                 store=True)
    currency_id = fields.Many2one(related='quotation_id.currency_id', store=True, string='Currency', readonly=True)
    date_quotation = fields.Datetime(related='quotation_id.date_quotation', string='Quotation Date', readonly=True)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    _sql_constraints = [
        ('accountable_required_fields',
         "CHECK(display_type IS NOT NULL OR (product_id IS NOT NULL AND product_uom IS NOT NULL AND date_planned IS NOT NULL))",
         "Missing required fields on accountable purchase quotation line."),
        ('non_accountable_null_fields',
         "CHECK(display_type IS NULL OR (product_id IS NULL AND price_unit = 0 AND product_uom_qty = 0 AND product_uom IS NULL AND date_planned is NULL))",
         "Forbidden values on non-accountable purchase quotation line"),
    ]

    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase quotations.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        return {
            'price_unit': self.price_unit,
            'currency_id': self.quotation_id.currency_id,
            'product_qty': self.product_qty,
            'product': self.product_id,
            'partner': self.quotation_id.partner_id,
        }

    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            fpos = line.quotation_id.fiscal_position_id or line.quotation_id.fiscal_position_id.get_fiscal_position(
                line.quotation_id.partner_id.id)
            # filter taxes by company
            taxes = line.product_id.supplier_taxes_id.filtered(lambda r: r.company_id == line.env.company)
            line.taxes_id = fpos.map_tax(taxes, line.product_id, line.quotation_id.partner_id)

    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity')
    def _compute_qty_invoiced(self):
        for line in self:
            qty = 0.0
            for inv_line in line.invoice_lines:
                if inv_line.move_id.state not in ['cancel']:
                    if inv_line.move_id.move_type == 'in_invoice':
                        qty += inv_line.product_uom_id._compute_quantity(inv_line.quantity, line.product_uom)
                    elif inv_line.move_id.move_type == 'in_refund':
                        qty -= inv_line.product_uom_id._compute_quantity(inv_line.quantity, line.product_uom)
            line.qty_invoiced = qty

    @api.depends('product_id')
    def _compute_qty_received_method(self):
        for line in self:
            if line.product_id and line.product_id.type in ['consu', 'service']:
                line.qty_received_method = 'manual'
            else:
                line.qty_received_method = False

    @api.depends('qty_received_method', 'qty_received_manual')
    def _compute_qty_received(self):
        for line in self:
            if line.qty_received_method == 'manual':
                line.qty_received = line.qty_received_manual or 0.0
            else:
                line.qty_received = 0.0

    @api.onchange('qty_received')
    def _inverse_qty_received(self):
        """ When writing on qty_received, if the value should be modify manually (`qty_received_method` = 'manual' only),
            then we put the value in `qty_received_manual`. Otherwise, `qty_received_manual` should be False since the
            received qty is automatically compute by other mecanisms.
        """
        for line in self:
            if line.qty_received_method == 'manual':
                line.qty_received_manual = line.qty_received
            else:
                line.qty_received_manual = 0.0

    @api.model
    def create(self, values):
        if values.get('display_type', self.default_get(['display_type'])['display_type']):
            values.update(product_id=False, price_unit=0, product_uom_qty=0, product_uom=False, date_planned=False)

        quotation_id = values.get('quotation_id')
        if 'date_planned' not in values:
            quotation = self.env['purchase.quotation'].browse(quotation_id)
            if quotation.date_planned:
                values['date_planned'] = quotation.date_planned
        line = super(PurchaseQuotationLine, self).create(values)
        if line.quotation_id.state == 'purchase':
            msg = _("Extra line with %s ") % (line.product_id.display_name,)
            line.quotation_id.message_post(body=msg)
        return line

    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(
                _("You cannot change the type of a purchase quotation line. Instead you should delete the current line and create a new line of the proper type."))

        if 'product_qty' in values:
            for line in self:
                if line.quotation_id.state == 'purchase':
                    line.quotation_id.message_post_with_view('purchase.track_po_line_template',
                                                             values={'line': line,
                                                                     'product_qty': values['product_qty']},
                                                             subtype_id=self.env.ref('mail.mt_note').id)
        return super(PurchaseQuotationLine, self).write(values)

    def unlink(self):
        for line in self:
            if line.quotation_id.state in ['purchase', 'done']:
                raise UserError(_('Cannot delete a purchase quotation line which is in state \'%s\'.') % (line.state,))
        return super(PurchaseQuotationLine, self).unlink()

    @api.model
    def _get_date_planned(self, seller, po=False):
        """Return the datetime value to use as Schedule Date (``date_planned``) for
           PO Lines that correspond to the given product.seller_ids,
           when quotationed at `date_quotation_str`.

           :param Model seller: used to fetch the delivery delay (if no seller
                                is provided, the delay is 0)
           :param Model po: purchase.quotation, necessary only if the PO line is
                            not yet attached to a PO.
           :rtype: datetime
           :return: desired Schedule Date for the PO line
        """
        date_quotation = po.date_quotation if po else self.quotation_id.date_quotation
        if date_quotation:
            return date_quotation + relativedelta(days=seller.delay if seller else 0)
        else:
            return datetime.today() + relativedelta(days=seller.delay if seller else 0)

    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.product_id:
            return

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.price_unit = self.product_qty = 0.0

        self._product_id_change()

        self._suggest_quantity()
        self._onchange_quantity()

    def _product_id_change(self):
        if not self.product_id:
            return

        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        product_lang = self.product_id.with_context(
            lang=get_lang(self.env, self.partner_id.lang).code,
            partner_id=self.partner_id.id,
            company_id=self.company_id.id,
        )
        self.name = self._get_product_purchase_description(product_lang)

        self._compute_tax_id()

    @api.onchange('product_id')
    def onchange_product_id_warning(self):
        if not self.product_id or not self.env.user.has_group('purchase.group_warning_purchase'):
            return
        warning = {}
        title = False
        message = False

        product_info = self.product_id

        if product_info.purchase_line_warn != 'no-message':
            title = _("Warning for %s") % product_info.name
            message = product_info.purchase_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            if product_info.purchase_line_warn == 'block':
                self.product_id = False
            return {'warning': warning}
        return {}

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        if not self.product_id:
            return
        params = {'quotation_id': self.quotation_id}
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.quotation_id.date_quotation and self.quotation_id.date_quotation.date(),
            uom_id=self.product_uom,
            params=params)

        if seller or not self.date_planned:
            self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        if not seller:
            if self.product_id.seller_ids.filtered(lambda s: s.name.id == self.partner_id.id):
                self.price_unit = 0.0
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price,
                                                                             self.product_id.supplier_taxes_id,
                                                                             self.taxes_id,
                                                                             self.company_id) if seller else 0.0
        if price_unit and seller and self.quotation_id.currency_id and seller.currency_id != self.quotation_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.quotation_id.currency_id, self.quotation_id.company_id,
                self.date_quotation or fields.Date.today())

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit

    @api.depends('product_uom', 'product_qty', 'product_id.uom_id')
    def _compute_product_uom_qty(self):
        for line in self:
            if line.product_id and line.product_id.uom_id != line.product_uom:
                line.product_uom_qty = line.product_uom._compute_quantity(line.product_qty, line.product_id.uom_id)
            else:
                line.product_uom_qty = line.product_qty

    def _suggest_quantity(self):
        '''
        Suggest a minimal quantity based on the seller
        '''
        if not self.product_id:
            return
        seller_min_qty = self.product_id.seller_ids \
            .filtered(
            lambda r: r.name == self.quotation_id.partner_id and (not r.product_id or r.product_id == self.product_id)) \
            .sorted(key=lambda r: r.min_qty)
        if seller_min_qty:
            self.product_qty = seller_min_qty[0].min_qty or 1.0
            self.product_uom = seller_min_qty[0].product_uom
        else:
            self.product_qty = 1.0

    def _get_product_purchase_description(self, product_lang):
        self.ensure_one()
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase

        return name

    def _prepare_account_move_line(self, move):
        self.ensure_one()
        if self.product_id.purchase_method == 'purchase':
            qty = self.product_qty - self.qty_invoiced
        else:
            qty = self.qty_received - self.qty_invoiced
        if float_compare(qty, 0.0, precision_rounding=self.product_uom.rounding) <= 0:
            qty = 0.0

        return {
            'name': '%s: %s' % (self.quotation_id.name, self.name),
            'move_id': move.id,
            'currency_id': move.currency_id.id,
            'purchase_line_id': self.id,
            'date_maturity': move.invoice_date_due,
            'product_uom_id': self.product_uom.id,
            'product_id': self.product_id.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'partner_id': move.commercial_partner_id.id,
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'display_type': self.display_type,
        }


class LastFivePurchase(models.TransientModel):
    _name = 'last.five.purchase'

    last_purchase_id = fields.Many2one('purchase.quotation', 'last_purchase_ids')
    product_id = fields.Many2one('product.product')
    vendor_id = fields.Many2one('res.partner', 'Vendor')
    price = fields.Float('Price')
    product_qty = fields.Integer('Quantity')
    date_planned = fields.Date('Date')


class StockDetails(models.TransientModel):
    _name = 'show.stock.details'

    stock_details_ids = fields.Many2one('purchase.quotation', 'stock_details_id')
    location_id = fields.Many2one('stock.location')
    available_quantity = fields.Float('Available Quantity')
    quantity = fields.Float('Price')
    company_id = fields.Many2one('res.company')
