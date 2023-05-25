from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_area= fields.Selection([
        ('0', 'Square Feet'),
        ('1', ' Square Meter'),
    ], 'Weight unit of measure', config_parameter='product.area_in_square_meter', default='0')
