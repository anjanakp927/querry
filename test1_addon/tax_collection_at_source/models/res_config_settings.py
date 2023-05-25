from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_turnover = fields.Float(string="Turn over", related="company_id.company_turnover", readonly=False)
    transaction_amount = fields.Float(string="Transaction Amount", related="company_id.transaction_amount", readonly=False)

    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('company_turnover',
                                                         self.company_turnover)
        self.env['ir.config_parameter'].sudo().set_param('transaction_amount',
                                                         self.transaction_amount)
        super(ResConfigSettings, self).set_values()

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            company_turnover=self.env['ir.config_parameter'].sudo().get_param('company_turnover', default=0),
            transaction_amount=self.env['ir.config_parameter'].sudo().get_param('transaction_amount', default=0),
        )
        return res

class ResCompany(models.Model):
    _inherit = 'res.company'

    company_turnover = fields.Float()
    transaction_amount = fields.Float()