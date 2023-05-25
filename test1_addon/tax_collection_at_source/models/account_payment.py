

from odoo import api, fields, models, _


class tcs_accounts(models.Model):
    _name = 'tcs.accountss'

    tcs_account_id = fields.Many2one('account.account', string="Difference Account",
                                     domain=[('deprecated', '=', False)], copy=False, required="1")
    name = fields.Char('Description')
    amt_percent = fields.Float(string='Amount(%)', digits=(16, 2))
    amount = fields.Monetary(string='Payment Amount', required=True)
    tax_id = fields.Many2one('account.tax', string='Tax', required=True, )
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    payment_id = fields.Many2one('account.payment', string='Payment Record')


class AccountPayment(models.Model):
    _inherit = "account.payment"

    tcs = fields.Boolean('TCS / Withholding', default=False)
    tcs_tax_ids = fields.Many2many('account.tax', string='TCS')
    tcs_amt = fields.Float(string='TCS Amount', compute='compute_tcs_amnt')
    tax_amount = fields.Float(string='TAX Amount')
    vendor_type = fields.Selection(related='partner_id.company_type', string='Partner Type')
    tcs_multi_acc_ids = fields.One2many('tcs.accountss', 'payment_id', string='Write Off Accounts')

    @api.model
    def default_get(self, fields):
        rec = super(AccountPayment, self).default_get(fields)
        print(rec.get('journal_id'),'99999999999999999999999999999999999999999999999999999999999999999999999999999')
        date = rec.get('date')
        if date:
            dates = self.env.user.company_id.compute_fiscalyear_dates(date)
            payments = self.env['account.payment'].search(
                [('state', '=', 'posted'), ('date', '>=', dates['date_from']), ('date', '<=', dates['date_to'])])
            payments
            journal_total = sum(payments.filtered(lambda c: c.payment_type == 'inbound').mapped('amount'))
            turn_over = self.env.company.company_turnover
            if journal_total >= turn_over:
                taxes = self.env['account.tax'].search([('tcs', '=', True)])
                if taxes:
                    rec['tcs'] = True
                    rec['tcs_tax_ids'] = taxes.ids
        return rec


    @api.onchange('tcs_tax_ids')
    def onchange_tcs_tax_ids(self):
        self.write({'tcs_multi_acc_ids':[(5,0,0)]})
        print(self.tcs_multi_acc_ids,"))))))))))))))))))))))))))))))))))))))))))))))))))")
        if not self._context.get('active_model'):
            return False
        amount_res = self.invoice_ids and self.invoice_ids[0].amount_residual
        applicable = False
        for tcs_tax in self.tcs_tax_ids:
            active_id = self._context.get('active_id')
            move = self.env['account.move'].browse(active_id)
            if move.partner_id and move.partner_id.tcs_threshold_check:
                applicable = self.check_turnover(move.partner_id.id, tcs_tax.tcs_payment_excess, amount_res)
            tax_repartition_lines = tcs_tax.invoice_repartition_line_ids.filtered(
                lambda x: x.repartition_type == 'tax')
            taxes = tcs_tax._origin.compute_all(
                amount_res)
            tcs_tax_amount = taxes['total_included'] - taxes[
                'total_excluded'] if taxes else 0.0
            if applicable:
                if tcs_tax.amount_type == 'group':
                    for child in tcs_tax.children_tax_ids:
                        tax_repartition_lines = child.invoice_repartition_line_ids.filtered(
                            lambda x: x.repartition_type == 'tax')
                        taxes = child._origin.compute_all(
                            self.amount)
                        tcs_tax_amount = taxes['total_included'] - taxes[
                            'total_excluded'] if taxes else 0.0
                        self.tcs_multi_acc_ids.create({
                            'tcs_account_id': tax_repartition_lines._origin.id and tax_repartition_lines._origin.account_id.id,
                            'name': child.name,
                            'tax_id': child.id,
                            'amount': tcs_tax_amount,
                            'payment_id': self.id
                        })
                else:
                    self.tcs_multi_acc_ids.create({
                        'tcs_account_id': tax_repartition_lines._origin.id and tax_repartition_lines._origin.account_id.id,
                        'name': tcs_tax.name,
                        'tax_id': tcs_tax._origin.id,
                        'amount': tcs_tax_amount,
                        'payment_id': self.id
                    })
        diff_amount = sum([line.amount for line in self.tcs_multi_acc_ids])
        self.write({
            'amount':amount_res - diff_amount,
            'tcs_amt':diff_amount,
            'payment_difference_handling':'reconcile',
        })


    @api.depends('tcs', 'tcs_tax_ids', 'amount')
    def compute_tcs_amnt(self):
        for payment in self:
            payment.tcs_amt = 0.0
            if payment.tcs and payment.tcs_tax_ids and payment.amount:
                # if payment.invoice_line_ids:
                #     payment.tcs_amt = sum([line.amount for line in payment.tcs_multi_acc_ids])
                #     continue
                # applicable = True
                total_tcs_tax_amount = 0.0
                for tax in payment.tcs_tax_ids:
                    # if payment.partner_id and payment.partner_id.tcs_threshold_check:
                    #     applicable = self.check_turnover(self.partner_id.id, tax.tcs_payment_excess, self.amount)
                    # if applicable:
                    taxes = tax._origin.compute_all(
                        payment.amount)
                    total_tcs_tax_amount += taxes['total_included'] - taxes[
                        'total_excluded'] if taxes else payment.amount * (tax.amount / 100)
                    payment.tcs_amt = total_tcs_tax_amount
                    payment.amount += total_tcs_tax_amount
                    # else:
                    #     payment.tcs_amt = 0.0
            else:
                payment.tcs_amt = 0.0

    def action_draft(self):
        super(AccountPayment, self).action_draft()
        self.write({'tcs': False})

    def check_turnover(self, partner_id, threshold, amount):
        if self.payment_type == 'outbound':
            domain = [('partner_id', '=', partner_id), ('account_id.internal_type', '=', 'payable'),
                      ('move_id.state', '=', 'posted'), ('account_id.reconcile', '=', True)]
            journal_items = self.env['account.move.line'].search(domain)
            print(journal_items, '*******************************journal_items***********************************************')

            credits = sum([item.credit for item in journal_items])
            credits += amount
            if credits >= threshold:
                return True
            else:
                return False
        elif self.payment_type == 'inbound':
            domain = [('partner_id', '=', partner_id), ('account_id.internal_type', '=', 'receivable'),
                      ('move_id.state', '=', 'posted'), ('account_id.reconcile', '=', True)]
            journal_items = self.env['account.move.line'].search(domain)
            debits = sum([item.debit for item in journal_items])
            debits += amount
            if debits >= threshold:
                return True
            else:
                return False

    def update_prepare_moves(self, all_move_vals):
        applicable = True
        for payment in self:
            if payment.currency_id == payment.company_id.currency_id:
                currency_id = False
            else:
                currency_id = payment.currency_id.id
            if payment.tcs and payment.tcs_tax_ids and payment.tcs_amt:
                tcs_tag = False
                tag_ids = []
                for tax in payment.tcs_tax_ids:
                    if payment.partner_id and payment.partner_id.tcs_threshold_check:
                        applicable = payment.check_turnover(payment.partner_id.id, tax.tcs_payment_excess,
                                                            payment.amount)
                    tax_repartition_lines = tax.invoice_repartition_line_ids.filtered(
                        lambda x: x.repartition_type == 'tax')
                    for line in all_move_vals[0].get('line_ids'):
                        tcs_tag = line[2].get('tcs_tag')
                    if payment.payment_type == 'outbound' and payment.partner_type == 'supplier' and applicable:
                        if tax.amount_type == 'group':
                            for child in tax.children_tax_ids:
                                taxes = child._origin.compute_all(
                                    payment.amount)
                                tcs_tax_amount = taxes['total_included'] - taxes[
                                    'total_excluded'] if taxes else 0
                                tax_repartition_lines = child.invoice_repartition_line_ids.filtered(
                                    lambda x: x.repartition_type == 'tax')
                                for tax_rec in taxes.get('taxes'):
                                    if child._origin.id == tax_rec.get('id'):
                                        tag_ids = (tax_rec.get('tag_ids'))
                                for rec in all_move_vals[0].get('line_ids'):
                                    if rec[2]['debit'] and not rec[2].get('tcs_tag'):
                                        rec[2]['debit'] = rec[2]['debit'] - tcs_tax_amount
                                debit = (child.amount * payment.amount / 100)
                                all_move_vals[0]['line_ids'].append((0, 0, {
                                    'name': child.name,
                                    'amount_currency': tcs_tax_amount,
                                    'currency_id': currency_id,
                                    'debit': tcs_tax_amount,
                                    'credit': 0,
                                    'date_maturity': payment.payment_date,
                                    'partner_id': payment.partner_id.id,
                                    'tcs_tag': True,
                                    'account_id': tax_repartition_lines.id and tax_repartition_lines.account_id.id,
                                    'payment_id': payment.id,
                                    'tax_ids': [(6, 0, tax.ids)],
                                    'tag_ids': [(6, 0, tag_ids)],
                                }))
                        else:
                            taxes = tax._origin.compute_all(
                                payment.amount)
                            tcs_tax_amount = taxes['total_included'] - taxes[
                                'total_excluded'] if taxes else 0
                            tag_ids = []
                            for tax_rec in taxes.get('taxes'):
                                if tax._origin.id == tax_rec.get('id'):
                                    tag_ids = (tax_rec.get('tag_ids'))
                            for rec in all_move_vals[0].get('line_ids'):
                                if rec[2]['debit'] and not rec[2].get('tcs_tag'):
                                    rec[2]['debit'] = rec[2]['debit'] - tcs_tax_amount
                            all_move_vals[0]['line_ids'].append((0, 0, {
                                'name': tax.name,
                                'amount_currency': tcs_tax_amount,
                                'currency_id': currency_id,
                                'debit': tcs_tax_amount,
                                'credit': 0,
                                'date_maturity': payment.payment_date,
                                'partner_id': payment.partner_id.id,
                                'tcs_tag': True,
                                'account_id': tax_repartition_lines.id and tax_repartition_lines.account_id.id,
                                'payment_id': payment.id,
                                'tax_ids': [(6, 0, tax.ids)],
                                'tag_ids': [(6, 0, tag_ids)],
                            }))
                    elif payment.payment_type == 'inbound' and payment.partner_type == 'customer' and applicable:
                        if tax.amount_type == 'group':
                            for child in tax.children_tax_ids:
                                taxes = child._origin.compute_all(
                                    payment.amount)
                                tcs_tax_amount = taxes['total_included'] - taxes[
                                    'total_excluded'] if taxes else 0
                                tax_repartition_lines = child.invoice_repartition_line_ids.filtered(
                                    lambda x: x.repartition_type == 'tax')
                                for tax_rec in taxes.get('taxes'):
                                    if child._origin.id == tax_rec.get('id'):
                                        tag_ids = (tax_rec.get('tag_ids'))
                                for rec in all_move_vals[0].get('line_ids'):
                                    if rec[2]['credit'] and not rec[2].get('tcs_tag'):
                                        rec[2]['credit'] = rec[2]['credit'] - tcs_tax_amount
                                all_move_vals[0]['line_ids'].append((0, 0, {
                                    'name': child.name,
                                    'amount_currency': tcs_tax_amount,
                                    'currency_id': currency_id,
                                    'debit': 0,
                                    'credit': tcs_tax_amount,
                                    'date_maturity': payment.payment_date,
                                    'partner_id': payment.partner_id.id,
                                    'tcs_tag': True,
                                    'account_id': tax_repartition_lines.id and tax_repartition_lines.account_id.id,
                                    'payment_id': payment.id,
                                    'tax_ids': [(6, 0, tax.ids)],
                                    'tag_ids': [(6, 0, tag_ids)],
                                }))
                        else:
                            taxes = tax._origin.compute_all(
                                payment.amount)
                            tcs_tax_amount = taxes['total_included'] - taxes[
                                'total_excluded'] if taxes else 0
                            for tax_rec in taxes.get('taxes'):
                                if tax._origin.id == tax_rec.get('id'):
                                    tag_ids = (tax_rec.get('tag_ids'))
                            for rec in all_move_vals[0].get('line_ids'):
                                if rec[2]['credit'] and not rec[2].get('tcs_tag'):
                                    rec[2]['credit'] = rec[2]['credit'] - tcs_tax_amount
                            all_move_vals[0]['line_ids'].append((0, 0, {
                                'name': tax.name,
                                'amount_currency': tcs_tax_amount,
                                'currency_id': currency_id,
                                'debit': 0,
                                'credit': tcs_tax_amount,
                                'date_maturity': payment.payment_date,
                                'partner_id': payment.partner_id.id,
                                'tcs_tag': True,
                                'account_id': tax_repartition_lines.id and tax_repartition_lines.account_id.id,
                                'payment_id': payment.id,
                                'tax_ids': [(6, 0, tax.ids)],
                                'tag_ids': [(6, 0, tag_ids)],
                            }))
            return all_move_vals

    def _prepare_payment_moves(self):
        all_move_vals = []
        for payment in self:
            if not payment.tcs:
                return super(AccountPayment, self)._prepare_payment_moves()
            if payment.tcs and self._context.get('active_model') and self._context.get(
                    'active_model') == 'account.move' :
                company_currency = payment.company_id.currency_id
                move_names = payment.move_name.split(
                    payment._get_move_name_transfer_separator()) if payment.move_name else None
                write_off_amount = payment.payment_difference_handling == 'reconcile' and -payment.payment_difference or 0.0
                if payment.payment_type in ('outbound', 'transfer'):
                    counterpart_amount = payment.amount
                    liquidity_line_account = payment.journal_id.default_debit_account_id
                else:
                    counterpart_amount = -payment.amount
                    liquidity_line_account = payment.journal_id.default_credit_account_id

                if payment.currency_id == company_currency:
                    balance = counterpart_amount
                    write_off_balance = write_off_amount
                    counterpart_amount = write_off_amount = 0.0
                    currency_id = False
                else:
                    balance = payment.currency_id._convert(counterpart_amount, company_currency, payment.company_id,
                                                           payment.payment_date)
                    write_off_balance = payment.currency_id._convert(write_off_amount, company_currency,
                                                                     payment.company_id,
                                                                     payment.payment_date)
                    currency_id = payment.currency_id.id

                if payment.journal_id.currency_id and payment.currency_id != payment.journal_id.currency_id:
                    liquidity_line_currency_id = payment.journal_id.currency_id.id
                    liquidity_amount = company_currency._convert(
                        balance, payment.journal_id.currency_id, payment.company_id, payment.payment_date)
                else:
                    liquidity_line_currency_id = currency_id
                    liquidity_amount = counterpart_amount
                rec_pay_line_name = ''
                if payment.payment_type == 'transfer':
                    rec_pay_line_name = payment.name
                else:
                    if payment.partner_type == 'customer':
                        if payment.payment_type == 'inbound':
                            rec_pay_line_name += _("Customer Payment")
                        elif payment.payment_type == 'outbound':
                            rec_pay_line_name += _("Customer Credit Note")
                    elif payment.partner_type == 'supplier':
                        if payment.payment_type == 'inbound':
                            rec_pay_line_name += _("Vendor Credit Note")
                        elif payment.payment_type == 'outbound':
                            rec_pay_line_name += _("Vendor Payment")
                    if payment.invoice_ids:
                        rec_pay_line_name += ': %s' % ', '.join(payment.invoice_ids.mapped('name'))

                if payment.payment_type == 'transfer':
                    liquidity_line_name = _('Transfer to %s') % payment.destination_journal_id.name
                else:
                    liquidity_line_name = payment.name
                move_vals = {
                    'date': payment.payment_date,
                    'ref': payment.communication,
                    'journal_id': payment.journal_id.id,
                    'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
                    'partner_id': payment.partner_id.id,
                    'line_ids': [
                        (0, 0, {
                            'name': rec_pay_line_name,
                            'amount_currency': counterpart_amount + write_off_amount,
                            'currency_id': currency_id,
                            'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                            'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.id,
                            'account_id': payment.destination_account_id.id,
                            'payment_id': payment.id,
                        }),
                        (0, 0, {
                            'name': liquidity_line_name,
                            'amount_currency': -liquidity_amount,
                            'currency_id': liquidity_line_currency_id,
                            'debit': balance < 0.0 and -balance or 0.0,
                            'credit': balance > 0.0 and balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.id,
                            'account_id': liquidity_line_account.id,
                            'payment_id': payment.id,
                        }),
                    ],
                }
                if write_off_balance and payment.tcs:
                    for woff_payment in payment.tcs_multi_acc_ids:
                        taxes = woff_payment.tax_id._origin.compute_all(
                            payment.amount)
                        tag_ids = []
                        for tax_rec in taxes.get('taxes'):
                            if  woff_payment.tax_id._origin.id == tax_rec.get('id'):
                                tag_ids = (tax_rec.get('tag_ids'))
                        write_off_amount = -woff_payment.amount if payment.payment_type == 'outbound' else woff_payment.amount
                        write_off_amount = payment.payment_difference_handling == 'reconcile' and -write_off_amount or 0.0
                        if payment.currency_id == company_currency:
                            write_off_balance = write_off_amount
                        else:
                            write_off_balance = payment.currency_id._convert(write_off_amount, company_currency,
                                                                             payment.company_id,
                                                                             payment.payment_date)
                        move_vals['line_ids'].append((0, 0, {
                            'name': woff_payment.name,
                            'amount_currency': -write_off_amount,
                            'currency_id': currency_id,
                            'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
                            'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.id,
                            'account_id': woff_payment.tcs_account_id.id,
                            'tax_ids': [(6, 0, woff_payment.tax_id.ids)],
                            'tag_ids': [(6, 0, tag_ids)],
                            'payment_id': payment.id,
                        }))
                elif write_off_balance:
                    # Write-off line.
                    move_vals['line_ids'].append((0, 0, {
                        'name': payment.writeoff_label,
                        'amount_currency': -write_off_amount,
                        'currency_id': currency_id,
                        'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
                        'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.commercial_partner_id.id,
                        'account_id': payment.writeoff_account_id.id,
                        'payment_id': payment.id,
                    }))
                if move_names:
                    move_vals['name'] = move_names[0]
                all_move_vals.append(move_vals)
                if payment.payment_type == 'transfer':
                    if payment.destination_journal_id.currency_id:
                        transfer_amount = payment.currency_id._convert(counterpart_amount,
                                                                       payment.destination_journal_id.currency_id,
                                                                       payment.company_id, payment.payment_date)
                    else:
                        transfer_amount = 0.0
                    transfer_move_vals = {
                        'date': payment.payment_date,
                        'ref': payment.communication,
                        'partner_id': payment.partner_id.id,
                        'journal_id': payment.destination_journal_id.id,
                        'line_ids': [
                            (0, 0, {
                                'name': payment.name,
                                'amount_currency': -counterpart_amount,
                                'currency_id': currency_id,
                                'debit': balance < 0.0 and -balance or 0.0,
                                'credit': balance > 0.0 and balance or 0.0,
                                'date_maturity': payment.payment_date,
                                'partner_id': payment.partner_id.id,
                                'account_id': payment.company_id.transfer_account_id.id,
                                'payment_id': payment.id,
                            }),
                            (0, 0, {
                                'name': _('Transfer from %s') % payment.journal_id.name,
                                'amount_currency': transfer_amount,
                                'currency_id': payment.destination_journal_id.currency_id.id,
                                'debit': balance > 0.0 and balance or 0.0,
                                'credit': balance < 0.0 and -balance or 0.0,
                                'date_maturity': payment.payment_date,
                                'partner_id': payment.partner_id.id,
                                'account_id': payment.destination_journal_id.default_credit_account_id.id,
                                'payment_id': payment.id,
                            }),
                        ],
                    }
                    if move_names and len(move_names) == 2:
                        transfer_move_vals['name'] = move_names[1]
                    all_move_vals.append(transfer_move_vals)
            elif payment.tcs and not self._context.get('active_model'):
                res = super(AccountPayment, self)._prepare_payment_moves()
                all_move_vals = payment.update_prepare_moves(res)
        return all_move_vals
