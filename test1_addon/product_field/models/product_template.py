from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    return_issued = fields.Boolean(string="Return Issued")
    recondition = fields.Boolean(string="Recondition")

    area = fields.Float(string="Area")
    area_uom_name = fields.Char(string='Area unit of measure label', compute='_compute_area_uom_name')
    ampere_hour = fields.Float(string="Ampere Hour (AH)")
    volt_ampere = fields.Float(string="Volt Ampere (VA)")
    volt_direct_current = fields.Float(string="Volt Direct Current (VDC)")
    maintenance_approval = fields.Boolean(string="Maintenance Approval")
    weighment = fields.Boolean(string="Weighment")
    weighm_nt = fields.Boolean(string="Weighm_nt")
    item_code = fields.Char(string="Item Code")
    item_type = fields.Selection([
        ('product', 'Product'),
        ('material', 'Material')
    ], string='Item Type')

    buy_back_price = fields.Monetary(string='Buyback Price')
    part_number = fields.Char(string='Part Number')
    purchase_authority = fields.Selection([
        ('local', 'Local'),
        ('central', 'Central')
    ], string='Purchase Authority')

    @api.model
    def _get_area_uom_id_from_ir_config_parameter(self):
        product_area_in_square_param = self.env['ir.config_parameter'].sudo().get_param('product.area_in_square_meter')
        if product_area_in_square_param == '1':
            return self.env.ref('product_field.product_uom_area_sq_meter')
        else:
            return self.env.ref('product_field.product_uom_area_sq_feet')

    @api.model
    def _get_area_uom_name_from_ir_config_parameter(self):
        return self._get_area_uom_id_from_ir_config_parameter().display_name

    def _compute_area_uom_name(self):
        self.area_uom_name = self._get_area_uom_name_from_ir_config_parameter()







