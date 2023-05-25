from odoo import models, fields, _


class SchoolProfile(models.Model):
    _name = "school.profile"

    # this required will make that blue in the field which make compalsary
    # def get_default_rank(self):
    #
    #     if 1 == 1:
    #         return 200
    #     else:
    #         return 100
    def default_establish_date(self):
        return fields.Date.today()

    sequence = fields.Integer()
    name = fields.Char("school name")
    email = fields.Char(string="Email", required=True, placeholder="abc@gmail.com")
    parent_name = fields.Char(string="Parent Name")
    phone = fields.Integer(string="Phone")
    # defualt true kodthal eappolm true aayirikm but can be change
    virtual_class = fields.Boolean("virtual class support?", default=True)
    school_rank = fields.Integer("Rank")
    # school_rank = fields.Integer("Rank", default=lambda lm: lm.get_default_rank())
    result = fields.Float("Result", readonly=True)
    address = fields.Text("Address", readonly=True)
    # establish_date = fields.Date("establish Date")
    # establish_date = fields.Date("establish Date",default=fields.Date.today())
    establish_date = fields.Date("establish Date", default=lambda lm: lm.default_establish_date())
    open_date = fields.Datetime("open Date")
    # document entering ,after entering and save we only see the download button not the file name so innorder to save the file name we use a field called file name
    document = fields.Binary("Documents")
    document_name = fields.Char("Document_name")
    school_image = fields.Image("Upload School Image", max_width=100, max_height=100)
    school_type = fields.Selection([('public', 'Public'), ('private', 'Private')], string='Type of School')
    school_description = fields.Html(string="Description")
    #     oru field ne depends cheyth veroru field work cheyyanamekil also we use computed field, here depend on the  school_type the auto rank should computed
    auto_rank = fields.Integer(compute='_auto_rank_populate', string='auto_rank')
    user_id = fields.Many2one('res.users', string='User')
    order_line = fields.One2many('purchase.order', 'order_ids', string='Order Lines',store=True)


    def button_click(self):
        pass

    def _auto_rank_populate(self):
        for rec in self:
            if rec.school_type == "private":
                rec.auto_rank = 50
            elif rec.school_type == "public":
                rec.auto_rank == 100
            else:
                rec.auto_rank = 0

    def action_whats_up_redirecting(self):
        msg='Hi Vishnumaya %s'
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s'% (self.phone,msg)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url,
        }
