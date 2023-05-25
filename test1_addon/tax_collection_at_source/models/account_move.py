from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, format_date, get_lang


class AccountMoveline(models.Model):
    _inherit = "account.move.line"

    tcs_tag = fields.Boolean("TCS Tag", default=False)
    tax_id = fields.Many2one('account.tax', string='Tax')


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def default_get(self, fields):
        rec = super(AccountMove, self).default_get(fields)
        date = rec.get('date')
        if date:
            type = ''
            dates = self.env.user.company_id.compute_fiscalyear_dates(date)
            moves = self.env['account.move'].search(
                [('state', '=', 'posted'), ('date', '>=', dates['date_from']), ('date', '<=', dates['date_to'])])
            transaction_amount = self.env.company.transaction_amount

            if not rec.get('journal_id'):
                current_model = self.env.context.get('active_model')
                journal_type = 'sale' if current_model == 'sale.order' else 'purchase'
            else:
                journal = self.env['account.journal'].browse(rec.get('journal_id'))
                journal_type = journal.type
            if journal_type == 'sale':
                rec['tcs'] = True
                sales_journal_total = sum(
                    moves.filtered(lambda c: c.journal_id.type == 'sale').mapped('amount_total_signed'))
                if sales_journal_total >= transaction_amount:
                    taxes = self.env['account.tax'].search([('tcs', '=', True)])
                    if taxes:
                        rec['tcs_tax_ids'] = taxes.ids
            elif journal_type == 'purchase':
                rec['tds'] = True
                purchase_journal_total = sum(
                    moves.filtered(lambda c: c.journal_id.type == 'purchase').mapped('amount_total_signed'))
                if abs(purchase_journal_total) >= transaction_amount:
                    taxes = self.env['account.tax'].search([('tds', '=', True)])
                    if taxes:
                        rec['tds_tax_ids'] = taxes.ids
        return rec


    tcs = fields.Boolean('Apply TCS')
    tds_tax_ids = fields.Many2many('account.tax', 'tds_tax_rel', string='TDS',
                                   states={'draft': [('readonly', False)]})
    tcs_tax_ids = fields.Many2many('account.tax', 'tcs_tax_rel', string='TCS',
                                   states={'draft': [('readonly', False)]})
    tcs_amt = fields.Monetary(string='TCS Amount',
                              readonly=True)
    tds_amt = fields.Monetary(string='TDS Amount',
                              readonly=True)
    total_gross = fields.Monetary(string='Total',
                                  store=True)
    amount_total = fields.Monetary(string='Net Total',
                                   store=True, readonly=True)
    vendor_type = fields.Selection(related='partner_id.company_type', string='Partner Type')
