# -*- coding: utf-8 -*-

from odoo import models, fields, api


class building_anj(models.Model):
    _name = 'building_anj.building_anj'
    _description = 'building_anj.building_anj'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    price = fields.One2many('price.price', 'price_ids')
    email = fields.Char('email')
    age = fields.Integer('Age')

    def action_send_mail(self):
        template = self.env.ref('building_anj.email_template_mail')
        for rec in self:
            template.send_mail(rec.id)

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

    def special_command(self):
        a = self.env["price.price"]
        product_id = self.create({
            'name': 'anjana',
            'value': 90,
            "price": [(0, 0, {'price': 50, },

                       ), (0, 0, {'price': 23, },

                           )]
        })

    def special_command2(self):
        # 6 eannu id ulla record ne line item thil ninnu deltete cheyyunnu
        self.write({"price": [(2, 6, 0)]})

    def special500(self):
        a = self.price.mapped('quantity')
        b = self.env['building_anj.building_anj']
        print(a, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(b.value, "bbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        # all clear aavan
        self.price = [(5, 0, 0)]

    def special10(self):
        # parent view il ninnu child nte values update cheyyam
        self.write({"price": [(1, 15, {
            "quantity": 100
        })]})
#         6,0,0 is used in the case of many to many
