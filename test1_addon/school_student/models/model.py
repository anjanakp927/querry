from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SchoolStudent(models.Model):
    _name = "school.student"
    # copy =False attribute is used when duplicating in action if we dont want the field name in duplication we can use the copy

    name = fields.Char("name", required=True, copy=False)
    school_id = fields.Many2one("school.profile", string='school')
    phone = fields.Char(string='Phone')
    user = fields.Many2many("school.profile", string="User")
    is_virtual_class = fields.Boolean(related='user.virtual_class', string='Virtual Class')
    # the below two fields is for curecy itself if we select INR in the currency field curresponding change occure in the fees field
    currency_id = fields.Many2one("res.currency", string="currency")
    student_fees = fields.Monetary(string='student fees')
    roll_no = fields.Char(string='Roll no')

    #     special field "reference field" combination of selection field and many to one
    ref_id = fields.Reference([('school.profile', 'School'), ('account.move', 'Invoice')], string='Reference')

    #     Hard delete and Soft delete, namuk oru record maathram tree view il kaananda but athu database il ninnu delete avukayum venda eankil namuk active = false kodthal mayhi
    active = fields.Boolean(string="Active", default=True)

    # #     create methode use cheyth record nte okke active true aakunu
    # @api.model
    # def create(self, values):
    #     rtn = super(SchoolStudent, self).create(SchoolStudent, self).create(values)
    #     rtn.active = True
    #     return rtn

    #     DUPLICATE cheyyumbo use cheynu
    def copy(self, default={}):
        # default['name'] = False
        rtn = super(SchoolStudent, self).copy(default=default)
        rtn.student_fees = 100
        return rtn

    # delete cheyyan vendi use cheyyunnu but delete cheyyumbo oru condition kodkkunu aa condition il ullath deldete cheyyan pattilla(this is permenent delete)
    def unlink(self):
        for stud in self:
            if stud.student_fees > 0:
                raise UserError(_("you can't delete this student profile"))
            rtn = super(SchoolStudent, self).unlink()
            return rtn

    # NAME_CREATE orm methode is used or hit when there is many2one and under that we have two option one is create it will create deed_management record another is create and edit which will give the pop up
    # create cheymbo varunna pop up il default values set cheyyanamenkil upayogikam

    # @api.model
    # def name_create(self, name):
    #     rtn = self.create({"name": name, 'email': "abc@gmal.com"})
    #     return rtn.name_get()[0]
    # DEFAULT_GET methode

    # @api.model
    # def default_get(self, fields_list=[]):
    #     rtn = super(SchoolStudent, self).default_get(fields_list)
    #     rtn['student_fees'] = 20000
    #     return rtn

    def wiz_open(self):
        # return self.env['ir.actions.act_window']._for_xml_id("school_student.student_fees_update_action")
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'student.fees.update.wizard',
            'view_mode': 'form',
            'target': 'deed_management'
        }

    # fetching values from the database------------------------>
    @api.model
    def create(self, vals):
        lst = []
        res = super(SchoolStudent, self).create(vals)
        self._cr.execute('''select name from school_student''')
        names = self._cr.fetchall()
        print("name-------------------->", names)
        # using mapped we get theentire
        a = self.env['school.student'].search([]).mapped('student_fees')
        b = self.env['school.student'].search([]).filtered(lambda lm: lm.student_fees > 0)
        for fee in a:
            lst.append(fee)

        print(a)
        print(b)
        print(lst)

        return res

    @api.model
    def _change_roll_number(self, add_string):
        "this model is used to add roll number to student profile"
        for stud in self.search([('roll_no', "=", False)]):
            stud.roll_no = add_string + "STD" + str(stud.id)

    #             the add string is for "eval values is to be added"
    def action_whats_up_redirecting(self):
        msg = 'Hi Vishnumaya'
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.phone, msg)
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url}


# SEARCH USEFULL CODES


# stud_obj=self.env['school.student']
# stud_obj.search([])------->(eallaa records um kittum)
# stud_obj.search([])------->(records nte eanam kittm)
# stud_obj.search(['id','=','3'])-------->(id=3 aaya record kittm )
# then athile fields um kittm

# for stud in stud_obj.search(['id','=','3']):
#      stud.name
#      stud.total_fees

# stud_obj.search(['total_fees','>','3'])

# for stud in stud_obj.search(['total_fees','>','3'],['total_fees','<','3']):
#      stud.total_fees

# for stud in stud_obj.search('|',['total_fees','>','3'],['total_fees','<','3']):
#      stud.total_fees
# for stud in stud_obj.search_count(['active','=',False]):


class SchoolProfile(models.Model):
    _inherit = "school.profile"

    school_list = fields.One2many("school.student", 'school_id', string='school List')
