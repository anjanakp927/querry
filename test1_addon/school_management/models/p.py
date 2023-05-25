from odoo import models, fields, _


class SchoolProfile(models.Model):
    _inherit = "purchase.order"

    order_ids = fields.Many2one("school.profile")
