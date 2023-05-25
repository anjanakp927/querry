import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class HrEmployeeCreateAPI(models.Model):
    _name = 'employee.api.create'

    @api.model
    def action_create_employee(self, vals):

        hr_employee_val = {}
        hr_employee_contract_val = {}
        val = {}
        hr_employee_update_vals = {}
        employee = None
        event_type = ''

        if 'event_type' in vals:
            event_type = (vals.get('event_type'))

        if 'name' in vals:
            name = (vals.get('name'))
            hr_employee_val.update({'name': name or False})

        if 'employee_id' in vals:
            employee_id = (vals.get('employee_id'))

        if 'employee_no' in vals:
            employee_no = (vals.get('employee_no'))
            hr_employee_val.update({'employee_no': employee_no or False})

        if 'emp_category' in vals:
            emp_category = (vals.get('emp_category'))
            category = self.env['hr.employee.category'].search([('name', '=', emp_category)])

            if category:
                hr_employee_val.update({'category_id': category.id or False})

            else:
                val.update({'name': emp_category})
                category = self.env['hr.employee.category'].create(val)
                hr_employee_val.update({'category_id': category.id or False})

        if 'mobile_phone' in vals:
            mobile_phone = (vals.get('mobile_phone'))
            hr_employee_val.update({'mobile_phone': mobile_phone or False})

        if 'work_phone' in vals:
            work_phone = (vals.get('work_phone'))
            hr_employee_val.update({'work_phone': work_phone or False})

        if 'work_email' in vals:
            work_email = (vals.get('work_email'))
            hr_employee_val.update({'work_email': work_email or False})

        if 'company_id' in vals:
            company_id = int(vals.get('company_id', False))
            hr_employee_val.update({'company_id': company_id or False})
            hr_employee_update_vals.update({'company_id': company_id or False})

        if 'department' in vals:
            department = (vals.get('department'))
            dep = self.env['hr.department'].search([('name', '=', department)])
            if dep:
                hr_employee_val.update({'department_id': dep.id or False})
            else:
                val.update({'name': department})
                department = self.env['hr.department'].create(val)
                hr_employee_val.update({'department_id': department.id or False})

        if 'manager_id' in vals:
            manager_id = int(vals.get('manager_id'))
            hr_employee_val.update({'parent_id': manager_id or False})
            hr_employee_update_vals.update({'parent_id': manager_id or False})

        if 'coach_id' in vals:
            coach_id = int(vals.get('coach_id'))
            hr_employee_val.update({'coach_id': coach_id or False})

        if 'job_position' in vals:
            job_position = (vals.get('job_position'))
            if job_position:
                job = self.env['hr.job'].search([('name', '=', job_position)])
                if job:
                    hr_employee_val.update({'job_id': job.id or False})
                else:
                    val.update({'name': job_position})
                    job = self.env['hr.job'].create(val)
                    hr_employee_val.update({'job_id': job.id or False})

        if 'nationality' in vals:
            nationality = int(vals.get('nationality', False))
            hr_employee_val.update({'country_id': nationality or False})

        if 'identification_number' in vals:
            identification_number = (vals.get('identification_number', False))
            hr_employee_val.update({'identification_id': identification_number or False})

        if 'passport_number' in vals:
            passport_number = (vals.get('passport_number', False))
            hr_employee_val.update({'passport_id': passport_number or False})

        if 'gender' in vals:
            gender = (vals.get('gender', False))
            hr_employee_val.update({'gender': gender or False})

        if 'birthday' in vals:
            birthday = (vals.get('birthday', False))
            hr_employee_val.update({'birthday': birthday or False})

        if 'place_of_birth' in vals:
            place_of_birth = (vals.get('place_of_birth', False))
            hr_employee_val.update({'place_of_birth': place_of_birth or False})

        if 'country_of_birth' in vals:
            country_of_birth = int(vals.get('country_of_birth', False))
            hr_employee_val.update({'country_of_birth': country_of_birth or False})

        if 'marital_status' in vals:
            marital_status = (vals.get('marital_status', False))
            hr_employee_val.update({'marital': marital_status or False})

        if 'aadhar_no' in vals:
            aadhar_no = (vals.get('aadhar_no', False))
            hr_employee_val.update({'aadhar_no': aadhar_no or False})

        if 'identification_mark' in vals:
            identification_mark = (vals.get('identification_mark', False))
            hr_employee_val.update({'identification_mark': identification_mark or False})

        if 'driving_licence' in vals:
            driving_licence = (vals.get('driving_licence', False))
            hr_employee_val.update({'driving_licence': driving_licence or False})

        if 'driving_licence_validity' in vals:
            driving_licence_validity = (vals.get('driving_licence_validity', False))
            hr_employee_val.update({'driving_licence_validity': driving_licence_validity or False})

        if 'driving_licence_attachment' in vals:
            driving_licence_attachment = (vals.get('driving_licence_attachment', False))
            hr_employee_val.update({'driving_licence_attachment': driving_licence_attachment or False})

        if 'pan' in vals:
            pan = (vals.get('pan', False))
            hr_employee_val.update({'pan': pan or False})

        if 'pan_validity' in vals:
            pan_validity = (vals.get('pan_validity', False))
            hr_employee_val.update({'pan_validity': pan_validity or False})

        if 'pan_card_attachment' in vals:
            pan_card_attachment = (vals.get('pan_card_attachment', False))
            hr_employee_val.update({'pan_card_attachment': pan_card_attachment or False})

        if 'voter_id' in vals:
            voter_id = (vals.get('voter_id', False))
            hr_employee_val.update({'voter_id': voter_id or False})

        if 'voter_id_validity' in vals:
            voter_id_validity = (vals.get('voter_id_validity', False))
            hr_employee_val.update({'voter_id_validity': voter_id_validity or False})

        if 'voter_id_attachment' in vals:
            voter_id_attachment = (vals.get('voter_id_attachment', False))
            hr_employee_val.update({'voter_id_attachment': voter_id_attachment or False})

        if 'mines_certificate' in vals:
            mines_certificate = (vals.get('mines_certificate', False))
            hr_employee_val.update({'mines_certificate': mines_certificate or False})

        if 'mines_certificate_validity' in vals:
            mines_certificate_validity = (vals.get('mines_certificate_validity', False))
            hr_employee_val.update({'mines_certificate_validity': mines_certificate_validity or False})

        if 'mines_certificate_attachment' in vals:
            mines_certificate_attachment = (vals.get('mines_certificate_attachment', False))
            hr_employee_val.update({'mines_certificate_attachment': mines_certificate_attachment or False})

        if 'emergency_contact' in vals:
            emergency_contact = (vals.get('emergency_contact', False))
            hr_employee_val.update({'emergency_contact': emergency_contact or False})

        if 'emergency_phone' in vals:
            emergency_phone = (vals.get('emergency_phone', False))
            hr_employee_val.update({'emergency_phone': emergency_phone or False})

        if 'badge_number' in vals:
            badge_number = (vals.get('badge_number', False))
            hr_employee_val.update({'barcode': badge_number or False})

        if 'photo' in vals:
            photo = (vals.get('photo', False))
            hr_employee_val.update({'image_1920': photo or False})

        if 'pf_date' in vals:
            pf_date = (vals.get('pf_date', False))
            hr_employee_val.update({'pf_date': pf_date or False})

        if 'uan_no' in vals:
            uan_no = (vals.get('uan_no', False))
            hr_employee_val.update({'uan_no': uan_no or False})

        if 'nominee' in vals:
            nominee = (vals.get('nominee', False))
            hr_employee_val.update({'nominee': nominee or False})

        if 'cpf' in vals:
            cpf = (vals.get('cpf', False))
            hr_employee_val.update({'cpf': cpf or False})

        if 'lic_gratuity_no' in vals:
            lic_gratuity_no = (vals.get('lic_gratuity_no', False))
            hr_employee_val.update({'lic_gratuity_no': lic_gratuity_no or False})

        if 'esi_applicable' in vals:
            if vals["esi_applicable"] == 'true':
                hr_employee_val.update({'esi_active': 1})

        if 'esi_no' in vals:
            esi_no = (vals.get('esi_no', False))
            hr_employee_val.update({'esi_no': esi_no or False})

        if 'esi_join_date' in vals:
            esi_join_date = (vals.get('esi_join_date', False))
            hr_employee_val.update({'esi_join_date': esi_join_date or False})

        if 'esi_last_date' in vals:
            esi_last_date = (vals.get('esi_last_date', False))
            hr_employee_val.update({'esi_last_date': esi_last_date or False})

        if 'esi_exit_reason' in vals:
            val = {}
            esi_exit_reason = (vals.get('esi_exit_reason'))

            exit_reason = self.env['hr.welfare.master'].search([('name', '=', esi_exit_reason)])
            if exit_reason:
                hr_employee_val.update({'esi_exit_reason': exit_reason.id or False})
            else:
                val.update({'name': esi_exit_reason})
                exit_reason = self.env['hr.welfare.master'].create(val)
                hr_employee_val.update({'esi_exit_reason': exit_reason.id or False})

        if 'religion' in vals:
            val = {}
            religion = (vals.get('religion'))
            rel = self.env['hr.religion.master'].search([('name', '=', religion)])
            if rel:
                hr_employee_val.update({'religion_id': rel.id or False})
            else:
                val.update({'name': religion})
                rel = self.env['hr.religion.master'].create(val)
                hr_employee_val.update({'religion_id': rel.id or False})

        if 'language_lines' in vals:
            language_line = vals.get('language_lines')
            language_request_pos = 0
            language_request_line_det = []
            for language_request_item in language_line:
                language_request_line_items = {}

                if 'language' in language_request_item:
                    language_name = (language_request_item.get('language'))
                    language = self.env['hr.language'].search([('name', '=', language_name)])
                else:
                    val.update({'name': language_line['language']})
                    language = self.env['hr.language'].create(val)

                language_request_line_items.update({'language': language.id})

                if 'language_read' in language_request_item:
                    if language_request_item["language_read"] == 'true':
                        language_request_line_items.update({'language_read': 1})

                if 'language_speak' in language_request_item:
                    if language_request_item["language_speak"] == 'true':
                        language_request_line_items.update({'language_speak': 1})

                if 'language_write' in language_request_item:
                    if language_request_item["language_write"] == 'true':
                        language_request_line_items.update({'language_write': 1})

                if 'mother_tongue' in language_request_item:
                    if language_request_item["mother_tongue"] == 'true':
                        language_request_line_items.update({'mother_tongue': 1})

                language_request_line_det.append((0, language_request_pos, language_request_line_items))
                language_request_pos = language_request_pos + 1
            _logger.info("Service API :Language Lines Details (%s)", language_request_line_det)

            hr_employee_val.update({"employee_language_ids": language_request_line_det})

        if 'experience_line' in vals:
            experience_line = vals.get('experience_line')
            experience_pos = 0
            experience_line_det = []

            for items in experience_line:
                experience_line_items = {}
                experience_line_items.update({'job_id': (items['job_title'])})
                experience_line_items.update({'location': (items['location'])})
                experience_line_items.update({'from_date': str(items['start_date'])})
                experience_line_items.update({'to_date': str(items['end_date'])})
                experience_line_items.update({'company': (items['company'])})
                experience_line_items.update({'state_id': int(items['state_id'])})
                experience_line_items.update({'country_id': int(items['country_id'])})
                if items["relevance"] == 'true':
                    experience_line_items.update({'relevant_to_job': 1})

                experience_line_det.append((0, experience_pos, experience_line_items))

                experience_pos = experience_pos + 1
                _logger.info("Service API :Experience Lines Details (%s)", experience_line_det)
                hr_employee_val.update({"profession_ids": experience_line_det})
        if 'address' in vals:
            val = {}
            bank_val = {}
            address_line = vals.get('address')
            val.update(
                {'name': address_line['name'], 'street': address_line['street'], 'street2': address_line['street2'],
                 'city': address_line['city'], 'state_id': int(address_line['state_id']),
                 'country_id': int(address_line['country_id']),
                 'zip': address_line['zip'], 'phone': address_line['phone'], 'mobile': address_line['mobile'],
                 'email': address_line['email']})
            partner = self.env['res.partner'].create(val)

            if 'bank_details' in vals:
                bank_line = vals.get('bank_details')
                account_val = {}
                bank_ifsc = self.env['res.bank'].search([('bic', '=', bank_line['bank_ifsc_code'])])
                if bank_ifsc:
                    account_val.update(
                        {'acc_number': bank_line['bank_account_number'], 'partner_id': partner.id,
                         'bank_id': bank_ifsc.id})
                    bank_account = self.env['res.partner.bank'].create(account_val)
                else:
                    if bank_line['bank_ifsc_code']:
                        bank_val.update({'bic': bank_line['bank_ifsc_code']})

                    if bank_line['bank_name']:
                        bank_val.update({'name': bank_line['bank_name']})
                        if 'bank_street' in bank_line:
                            bank_val.update({'street': bank_line['bank_street']})
                        if 'bank_street2' in bank_line:
                            bank_val.update({'street2': bank_line['bank_street2']})
                        if 'bank_city' in bank_line:
                            bank_val.update({'city': bank_line['bank_city']})
                        if 'bank_state_id' in bank_line:
                            bank_val.update({'state': bank_line['bank_state_id']})
                        if 'bank_country_id' in bank_line:
                            bank_val.update({'country': bank_line['bank_country_id']})
                        if 'bank_phone' in bank_line:
                            bank_val.update({'phone': bank_line['bank_phone']})

                        if 'bank_zip' in bank_line:
                            bank_val.update({'zip': bank_line['bank_zip']})

                        if 'bank_email' in bank_line:
                            bank_val.update({'email': bank_line['bank_email']})

                        bank_id = self.env['res.bank'].create(bank_val)
                        if 'account_holder_name' in bank_line:
                            account_val.update({'acc_holder_name': bank_line['account_holder_name']})
                        account_val.update(
                            {'acc_number': bank_line['bank_account_number'], 'partner_id': partner.id,
                             'bank_id': bank_id.id})
                    bank_account = self.env['res.partner.bank'].create(account_val)
                hr_employee_val.update({'bank_account_id': bank_account.id or False})
                hr_employee_val.update({'address_home_id': partner.id or False})

            if 'educational_qualification' in vals:
                edu_line = vals.get('educational_qualification')
                edu_detail = []
                qualification_pos = 0
                val = {}

                for items in edu_line:
                    qualification_line = {}
                    qual = self.env['hr.recruitment.degree'].search([('name', '=', items['qualification'])])
                    if qual:
                        qualification_line.update({'type_id': qual.id or False})
                    else:
                        val.update({'name': items['qualification']})
                        qual = self.env['hr.recruitment.degree'].create(val)
                        qualification_line.update({'type_id': qual.id or False})

                    institute = self.env['hr.institute'].search([('name', '=', items['institute'])])
                    if institute:
                        qualification_line.update({'institute_id': institute.id or False})

                    else:
                        institute_val = {}
                        institute_val.update({'name': items['institute']})
                        institute = self.env['hr.institute'].create(val)
                        qualification_line.update({'institute_id': institute.id or False})

                    if 'score' in items:
                        qualification_line.update({'score': items['score'] or False})

                    if 'qualified_year' in items:
                        qualification_line.update({'qualified_year': items['year'] or False})

                    edu_detail.append((0, qualification_pos, qualification_line))
                    qualification_pos = qualification_pos + 1
                    hr_employee_val.update({"education_ids": edu_detail})

            if 'certificate' in vals:
                val = {}
                certificate_line = vals.get('certificate')
                certificate_detail = []
                certificate_pos = 0

                for items in certificate_line:

                    qualification_line = {}
                    cert = self.env['cert.cert'].search([('name', '=', items['course_name'])])
                    if cert:
                        qualification_line.update({'course_id': cert.id})
                    else:
                        val.update({'name': items['course_name']})
                        cert = self.env['cert.cert'].create(val)
                        qualification_line.update({'course_id': cert.id or False})

                    if 'year' in items:
                        qualification_line.update({'year': items['year'] or False})

                    if 'level' in items:
                        qualification_line.update({'levels': items['level'] or False})

                    certificate_detail.append((0, certificate_pos, qualification_line))
                    certificate_pos = certificate_pos + 1
                    hr_employee_val.update({"certification_ids": certificate_detail})

            if 'mines_wage_for_a_day' in vals:
                mines_wage_for_a_day = float(vals.get('mines_wage_for_a_day', False))
                hr_employee_val.update({'wage_for_a_day': mines_wage_for_a_day})

            if 'status' in vals:
                status = (vals.get('status', False))
                hr_employee_val.update({'mines_status': status})

            if 'gstin' in vals:
                gstin = (vals.get('gstin', False))
                hr_employee_val.update({'gstin': gstin})

            if 'pf_retire_date' in vals:
                pf_retire_date = (vals.get('pf_retire_date', False))
                hr_employee_val.update({'pf_retire_date': pf_retire_date})

            if 'basic_da' in vals:
                basic_da = float(vals.get('basic_da', False))
                hr_employee_val.update({'basic_da': basic_da})

            if 'food_allowance' in vals:
                food_allowance = float(vals.get('food_allowance', False))
                hr_employee_val.update({'food_allowance': food_allowance})

            if 'other_allowance' in vals:
                other_allowance = float(vals.get('other_allowance', False))
                hr_employee_val.update({'other_allowance': other_allowance})

            if 'mines_form_sl_no' in vals:
                mines_form_sl_no = (vals.get('mines_form_sl_no', False))
                hr_employee_val.update({'mines_form_sl_no': mines_form_sl_no or False})

            if 'mines_working_unit' in vals:
                mines_working_unit = (vals.get('mines_working_unit', False))
                hr_employee_val.update({'mines_working_unit': mines_working_unit or False})

            if 'labour_code' in vals:
                labour_code = (vals.get('labour_code', False))
                hr_employee_val.update({'pltn_labour_code': labour_code})

            if 'division' in vals:
                division = (vals.get('division', False))
                hr_employee_val.update({'pltn_division': division})

            if 'designation_group' in vals:
                designation_group = (vals.get('designation_group', False))
                hr_employee_val.update({'pltn_designation_group': designation_group})

            if 'need_weekly_cash_payment' in vals:
                if vals['need_weekly_cash_payment'] == 'true':
                    hr_employee_val.update({'pltn_is_weekly_cash_payment': 1})

            if 'from_date' in vals:
                from_date = (vals.get('from_date', False))
                hr_employee_val.update({'pltn_from_date': from_date})

            if 'basic' in vals:
                basic = float(vals.get('basic', False))
                hr_employee_val.update({'pltn_basic': basic})

            if 'da' in vals:
                da = float(vals.get('da', False))
                hr_employee_val.update({'pltn_da': da})

            if 'ot_rate' in vals:
                ot_rate = float(vals.get('ot_rate', False))
                hr_employee_val.update({'pltn_ot_rate': ot_rate})

            if 'weightage' in vals:
                weightage = float(vals.get('weightage', False))
                hr_employee_val.update({'pltn_weightage': weightage})

            if 'pf_allotted' in vals:
                if vals['pf_allotted'] == 'true':
                    hr_employee_val.update({'pltn_pf_allotted': 1})

            if 'pf_ac_no' in vals:
                pf_ac_no = (vals.get('pf_ac_no', False))
                hr_employee_val.update({'pltn_pf_ac_no': pf_ac_no})

            if 'probation' in vals:
                if vals['probation'] == 'true':
                    hr_employee_val.update({'pltn_is_probation': 1})

            if 'eligible_gratuity' in vals:
                eligible_gratuity = (vals.get('eligible_gratuity', False))
                hr_employee_val.update({'pltn_eligible_gratuity': eligible_gratuity})

            if 'thumb_req' in vals:
                if vals["thumb_req"] == "true":
                    hr_employee_val.update({'pltn_is_thumb': 1})

            if 'in_and_out_req' in vals:
                if vals["in_and_out_req"] == "true":
                    hr_employee_val.update({'pltn_is_in_out_time': 1})

            if 'branch_name' in vals:
                branch_name = (vals.get('branch_name', False))
                hr_employee_val.update({'pltn_branch_name': branch_name})

            if 'uniform_allotted' in vals:
                uniform_allotted = (vals.get('uniform_allotted', False))
                hr_employee_val.update({'pltn_uniform_allotted': uniform_allotted})

            if 'leaving_date' in vals:
                leaving_date = (vals.get('leaving_date', False))
                hr_employee_val.update({'pltn_leaving_date': leaving_date})

            if 'type_of_leave' in vals:
                type_of_leave = (vals.get('type_of_leave', False))
                hr_employee_val.update({'pltn_type_of_leave': type_of_leave})

            if 'type' in vals:
                type = (vals.get('type', False))
                hr_employee_val.update({'type': type or False})

            if 'residential_employee' in vals:
                if vals["residential_employee"] == 'true':
                    hr_employee_val.update({'residential_employee': 1 or False})

            if 'current_status' in vals:
                current_status = (vals.get('current_status'))
                hr_employee_val.update({'current_status': current_status or False})

            if 'retired' in vals:
                if vals["retired"] == 'true':
                    hr_employee_val.update({'retired': 1 or False})

            if 'mess_deduction' in vals:
                if vals["mess_deduction"] == 'true':
                    hr_employee_val.update({'mess_deduction': 1 or False})

            if 'show_in_payroll' in vals:
                if vals["show_in_payroll"] == 'true':
                    hr_employee_val.update({'show_in_payroll': 1 or False})

            if 'tds_required' in vals:
                if vals["tds_required"] == 'true':
                    hr_employee_val.update({'tds_required': 1 or False})

            if 'probation_start_date' in vals:
                probation_start_date = (vals.get('probation_start_date', False))
                hr_employee_val.update({'probation_start_date': probation_start_date or False})

            if 'probation_end_date' in vals:
                probation_end_date = (vals.get('probation_end_date', False))
                hr_employee_val.update({'probation_end_date': probation_end_date or False})

            if 'current_working_unit' in vals:
                current_working_unit = (vals.get('current_working_unit', False))
                hr_employee_val.update({'current_working_unit': current_working_unit or False})

            if 'current_firm' in vals:
                current_firm = (vals.get('current_firm', False))
                hr_employee_val.update({'current_firm': current_firm or False})

            if 'sub_firm' in vals:
                sub_firm = (vals.get('sub_firm', False))
                hr_employee_val.update({'sub_firm': sub_firm or False})

            if 'grade' in vals:
                grade = (vals.get('grade', False))
                hr_employee_val.update({'grade': grade or False})
            if 'estate_name' in vals:
                estate_name = (vals.get('estate_name', False))
                hr_employee_val.update({'estate_name': estate_name or False})

            if 'production_incentive_designation' in vals:
                production_incentive_designation = (vals.get('production_incentive_designation', False))
                hr_employee_val.update({'production_incentive_designation': production_incentive_designation or False})

            if 'leave_structure' in vals:
                leave_structure = (vals.get('leave_structure', False))
                hr_employee_val.update({'leave_structure': leave_structure or False})

            if 'remarks' in vals:
                remarks = (vals.get('remarks', False))
                hr_employee_val.update({'remarks': remarks or False})

            if 'mines_work_location' in vals:
                mines_work_location = (vals.get('mines_work_location', False))
                hr_employee_val.update({'mines_work_location': mines_work_location or False})

            if 'mines_position' in vals:
                mines_position = (vals.get('mines_position', False))
                hr_employee_val.update({'mines_position': mines_position or False})

            if 'mines_position_id' in vals:
                mines_position_id = (vals.get('mines_position_id', False))
                hr_employee_val.update({'mines_position_id': mines_position_id or False})

            if 'mines_classification' in vals:
                mines_classification = (vals.get('mines_classification', False))
                hr_employee_val.update({'mines_classification': mines_classification or False})

            if 'labour_category' in vals:
                labour_category = (vals.get('labour_category', False))
                hr_employee_val.update({'labour_category': labour_category or False})

            if 'exit_date' in vals:
                exit_date = (vals.get('exit_date', False))
                hr_employee_val.update({'pltn_leaving_date': exit_date or False})

            if 'work_location' in vals:
                work_location = (vals.get('work_location', False))
                hr_employee_val.update({'work_location': work_location or False})

            if 'date_of_firm_join' in vals:
                date_of_firm_join = (vals.get('date_of_firm_join', False))
                hr_employee_val.update({'mines_date_of_join_firm': date_of_firm_join or False})

            if 'date_of_join' in vals:
                date_of_join = (vals.get('date_of_join', False))
                hr_employee_val.update({'date_of_join': date_of_join or False})

            employee = False
            if event_type == 'create':
                employee = self.env['hr.employee'].create(hr_employee_val)

                contract_val = {}
                struct_val = {}
                struct_type_val = {}

                if 'emp_history' in vals:
                    emp_history_val = {}
                    emp_history = (vals.get('emp_history', False))
                    for emp in employee:
                        emp_history_val.update({'name': emp.id})
                        emp_history_lines_pos = 0
                        emp_history_lines_line_det = []
                        for lines_item in emp_history:
                            emp_history_line_items = {}
                            emp_history_line_items.update(
                                {'field_name': (lines_item['fieldname']),
                                 'old_value': (lines_item['old_value']),
                                 'new_value': (lines_item['new_value']),
                                 'udate': (lines_item['udate'])})
                            emp_history_lines_line_det.append((0, emp_history_lines_pos, emp_history_line_items))
                            emp_history_lines_pos = emp_history_lines_pos + 1
                        emp_history_val.update({"emp_history_ids": emp_history_lines_line_det})
                        emp_history = self.env['hr.employee.history'].create(emp_history_val)

                # if 'hra' in vals:
                #     hra = (vals.get('hra', False))
                #     contract_val.update({'hra': hra})
                #
                # if 'tds' in vals:
                #     tds = (vals.get('tds', False))
                #     contract_val.update({'tds': tds})
                #
                # if 'room_rent' in vals:
                #     room_rent = (vals.get('room_rent', False))
                #     contract_val.update({'room_rent': room_rent})
                #
                # if 'canteen_deduction' in vals:
                #     canteen_deduction = (vals.get('canteen_deduction', False))
                #     contract_val.update({'canteen_deduction': canteen_deduction})
                #
                # if 'education_allowance' in vals:
                #     education_allowance = (vals.get('education_allowance', False))
                #     contract_val.update({'education_allowance': education_allowance})
                #
                # if 'education_allowance_max' in vals:
                #     education_allowance_max = (vals.get('education_allowance_max', False))
                #     contract_val.update({'education_allowance_yearly': education_allowance_max})
                #
                # if 'uniform_allowance' in vals:
                #     uniform_allowance = (vals.get('uniform_allowance', False))
                #     contract_val.update({'uniform_allowance': uniform_allowance})
                #
                # if 'washing_allowance' in vals:
                #     washing_allowance = (vals.get('washing_allowance', False))
                #     contract_val.update({'washing_allowance': washing_allowance})
                #
                # if 'meal_allowance' in vals:
                #     meal_allowance = (vals.get('meal_allowance', False))
                #     contract_val.update({'meal_allowance': meal_allowance})
                #
                # if 'lta_max' in vals:
                #     lta_max = (vals.get('lta_max', False))
                #     contract_val.update({'lta_max': lta_max})
                #
                # if 'servant_allowance' in vals:
                #     servant_allowance = (vals.get('servant_allowance', False))
                #     contract_val.update({'servant_allowance': servant_allowance})
                #
                # if 'conveyance_allowance' in vals:
                #     conveyance_allowance = (vals.get('conveyance_allowance', False))
                #     contract_val.update({'travel_allowance': conveyance_allowance})
                #
                # if 'special_allowance' in vals:
                #     special_allowance = (vals.get('special_allowance', False))
                #     contract_val.update({'other_allowance': special_allowance})
                #
                # if 'plantation_allowance' in vals:
                #     plantation_allowance = (vals.get('plantation_allowance', False))
                #     contract_val.update({'plantation_allowance': plantation_allowance})
                #
                # if 'composite_allowance' in vals:
                #     composite_allowance = (vals.get('composite_allowance', False))
                #     contract_val.update({'composite_allowance': composite_allowance})
                #
                # if 'petrol_allowance' in vals:
                #     petrol_allowance = (vals.get('petrol_allowance', False))
                #     contract_val.update({'petrol_allowance': petrol_allowance})
                #
                # if 'daily_allowance' in vals:
                #     daily_allowance = (vals.get('daily_allowance', False))
                #     contract_val.update({'over_day': daily_allowance})
                #
                # if 'kit_allowance' in vals:
                #     kit_allowance = (vals.get('kit_allowance', False))
                #     contract_val.update({'kit_allowance': kit_allowance})
                #
                # if 'phone_allowance' in vals:
                #     phone_allowance = (vals.get('phone_allowance', False))
                #     contract_val.update({'phone_allowance': phone_allowance})
                #
                if 'wage' in vals:
                    wage = (vals.get('wage', False))
                contract_val.update({'wage': '0'})
                #
                # if 'wage_type' in vals:
                #     wage_type = (vals.get('wage_type', False))
                #     contract_val.update({'wage_type': wage_type or False})

                if 'salary_structure_id' in vals:
                    salary_structure_id = (vals.get('salary_structure_id', False))
                    contract_val.update({'struct_id': salary_structure_id or False})

                if 'salary_advantage_details' in vals:
                    salary_advantage_details = (vals.get('salary_advantage_details', False))
                    lines_pos = 0
                    lines_line_det = []
                    for lines_item in salary_advantage_details:
                        salary_details_line_items = {}
                        salary_details_line_items.update(
                            {'advantage_template_id': (lines_item['id'])})
                        salary_details_line_items.update({'amount': float(lines_item['amount'])})
                        lines_line_det.append((0, lines_pos, salary_details_line_items))
                        lines_pos = lines_pos + 1
                    contract_val.update({"advantages_ids": lines_line_det})

                if 'salary_deduction_details' in vals:
                    salary_deduction_details = (vals.get('salary_deduction_details', False))
                    lines_pos = 0
                    lines_line_det = []
                    for lines_item in salary_deduction_details:
                        salary_details_line_items = {}
                        salary_details_line_items.update(
                            {'deduction_template_id': (lines_item['id'])})
                        salary_details_line_items.update({'amount': float(lines_item['amount'])})
                        lines_line_det.append((0, lines_pos, salary_details_line_items))
                        lines_pos = lines_pos + 1
                    contract_val.update({"deduction_ids": lines_line_det})
                if 'Salary_hike' in vals:
                    Salary_hike = (vals.get('Salary_hike', False))
                    for rec in Salary_hike:
                        struct_id = 0
                        calcflag = ''
                        Salary_hike_val = {}
                        for i in rec['sal_data']:
                            struct_id = (i['PayID'])
                            calcflag = (i['calcflag'])
                        Salary_hike_val.update(
                            {'name': employee.name + "/" + rec['Effective_date'], 'employee_id': employee.id,
                             'department_id': employee.department_id.id,
                             'job_id': employee.job_id.id,
                             'date_start': rec['Effective_date'],
                             'struct_id': struct_id,
                             'wage': (vals.get('wage')),
                             })
                        if calcflag == 'A':
                            lines_pos = 0
                            lines_line_det = []
                            for res in rec['sal_data']:
                                salary_details_line_items = {}
                                salary_details_line_items.update(
                                    {'advantage_template_id': (res['Advantage_Id'])})
                                salary_details_line_items.update({'amount': float(res['Amount'])})
                                lines_line_det.append((0, lines_pos, salary_details_line_items))
                                lines_pos = lines_pos + 1
                            Salary_hike_val.update({"advantages_ids": lines_line_det})
                        if calcflag == 'D':
                            lines_pos = 0
                            lines_line_det = []
                            for res in rec['sal_data']:
                                salary_details_line_items = {}
                                salary_details_line_items.update(
                                    {'deduction_template_id': (res['Advantage_Id'])})
                                salary_details_line_items.update({'amount': float(res['Amount'])})
                                lines_line_det.append((0, lines_pos, salary_details_line_items))
                                lines_pos = lines_pos + 1
                            Salary_hike_val.update({"deduction_ids": lines_line_det})
                        sal_hike = self.env['hr.contract'].create(Salary_hike_val)

                contract_val.update({'name': employee.name + "/" + vals['date_of_join'], 'employee_id': employee.id,
                                     'department_id': employee.department_id.id,
                                     'job_id': employee.job_id.id,
                                     'date_start': vals['date_of_join'],
                                     'state': vals.get('contract_state')})

                contract = self.env['hr.contract'].create(contract_val)

                if employee:
                    _logger.info("Service API : Employee Created")
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'employee_id': employee.id
                    })
                else:
                    status = 'FAILED'
                    status_code = 400
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'employee_id': 'NA'
                    })

            elif event_type == 'update':
                employee = self.env['hr.employee'].search([('id', '=', vals.get('employee_id'))])
                if employee:
                    employee.update(hr_employee_update_vals)
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'employee_id': employee.id

                    })
                else:
                    status = 'FAILED'
                    status_code = 400
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'employee_id': 'NA'
                    })
            else:
                status = 'INVALID TYPE'
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'employee_id': 'NA'
                })
