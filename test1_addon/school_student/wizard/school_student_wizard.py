from odoo import api, models, fields


class StudentFeesUpdateWizard(models.TransientModel):
    _name = "student.fees.update.wizard"

    total_fees = fields.Float('Fees')

    def update_student_fees(self):
        self.env['school.student'].brows(self._context.get('active_ids')).update({'total_fees': self.total_fees})
