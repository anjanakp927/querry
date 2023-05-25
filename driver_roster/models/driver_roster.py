
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DriverRoster(models.Model):
    _name = 'driver.roster'
    _description = 'driver_roster'

    driver = fields.Many2one('hr.employee', string='Driver', required=True)
    sale_order_ids = fields.Many2many('sale.order', string='Sale Order')
    code = fields.Char("Driver Roster Code", default='New')
    date = fields.Date(string='Date')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ], default='draft')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('driver.roster') or 'New'
        rtn = super(DriverRoster, self).create(vals)
        return rtn

    @api.onchange('date')
    def get_sale_orders_by_date(self):
        if self.date:
            orders = self.env['sale.order'].search([]).filtered(
                lambda sale: sale.date_order.date() == self.date)
            self.sale_order_ids = orders

    @api.constrains('sale_order_ids')
    def check_delivered_orders(self):
        for record in self:
            if len(record.sale_order_ids) < 1:
                raise ValidationError(_('Sale Order Should not be Empty'))

            assigned_sale_orders = self.env['driver.roster'].search(
                [('state', '=', 'confirm'), ('sale_order_ids', 'in', record.sale_order_ids.ids),
                 ('id', '!=', record.id)])
            if assigned_sale_orders:
                raise ValidationError(
                    _('sale orders are already assigned to another driver'))

    def button_confirm(self):
        self.state = 'confirm'

    def button_draft(self):
        self.state = 'draft'

    def cancel(self):
        self.state = 'cancel'

    def button_draft(self):
        self.state = 'draft'
