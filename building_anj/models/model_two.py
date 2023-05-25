
from odoo import models, fields, api
from lxml import etree


class building_anj(models.Model):
    _name = 'price.price'
    _description = 'building_anj.building_anj'

    name = fields.Char()
    quantity = fields.Integer()
    price = fields.Float()
    description = fields.Text()
    price_ids = fields.Many2one("building_anj.building_anj")
    rate = fields.Float()
    amount = fields.Float()


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(building_anj, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                           submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(result['arch'])
            name_field = doc.xpath("//field[@name='quantity']")
            print(name_field)
            if name_field:
                name_field[0].addnext(etree.Element('label', {
                    "string": "HHHHHHHHHHHH"
                }))
                result['arch'] = etree.tostring(doc, encoding="unicode")
            if name_field:
                name_field[0].addnext(etree.Element('field', {
                    "string": "rate",
                    "name": "rate"
                }))
                name_field[0].addnext(etree.Element('field', {
                    "string": "amount",
                    "name": "amount"
                }))
                result['arch'] = etree.tostring(doc, encoding="unicode")
        return result

