from odoo import models, fields, api, tools


class building_anj1(models.Model):
    _name = 'dbs.query'
    _description = 'db.query'
    _auto = False

    name = fields.Char()
    description = fields.Text()
    value = fields.Integer()
    quantity = fields.Integer()



    def init(self):
        tools.drop_view_if_exists(self._cr, 'dbs_query')
        self._cr.execute("""CREATE OR REPLACE VIEW dbs_query AS
           (SELECT row_number() over () as id ,line.name,line.description,line.value,line.quantity FROM( 
           SELECT prz.name,prz.description,prz.value,baj.quantity FROM building_anj_building_anj prz 
           LEFT JOIN price_price baj ON(prz.id=baj.price_ids))line 
           )""")
