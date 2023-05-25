import xmlrpc
import logging
import json
import xmlrpc.client
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class HrRequestControl(http.Controller):

    @http.route(['/hr_employee'], type='json', auth='public', methods=['POST'], csrf=False)
    def hms_partner_create(self, **post):

        _logger.info("Service API : Data Received, Processing ......")

        status_code = 500
        status = "REJECTED"

        if not post:
            _logger.info("Service API : No Data Received or Incorrect Data Format!")
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': "No Data Received or Incorrect Data Format!",
            })

        _logger.info("Service API : Raw Data (JSON) Log Created")

        params = post.copy()

        _logger.info("Service API : Raw Data (JSON) copied")

        if params:
            if not params.get('username', False) \
                    or not params.get('password', False) \
                    :
                _logger.info("Service API : Login Parameters Not Available. Returning")
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "Missing Parameters",
                })

            user_id = request.env['res.users'].sudo().search([('login', '=', str(params['username']))],
                                                             limit=1)
            # user_id.update({'company_id':int(params['company_id'])})
            _logger.info("Service API : Company IDs of User (%s)  (%s)", user_id.name, user_id.company_ids)
            if not user_id:
                _logger.info('Service API : User Not Available Returning')
                status_code = 400
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred - User Not Available",
                })

            log_vals = {}

            if 'event_type' in params:
                event_type = (params.get('event_type'))
                log_vals.update({'event_type': event_type or False})

            if 'employee_id' in params:
                employee_id = (params.get('employee_id'))
                log_vals.update({'employee_id': employee_id or False})

            if 'name' in params:
                name = (params.get('name'))
                log_vals.update({'name': name or False})

            if 'employee_no' in params:
                employee_no = (params.get('employee_no'))
                log_vals.update({'employee_no': employee_no or False})

            if 'job_title' in params:
                job_title = (params.get('job_title'))
                log_vals.update({'job_title': job_title or False})

            if 'emp_category' in params:
                emp_category = (params.get('emp_category'))
                log_vals.update({'emp_category': emp_category or False})

            if 'work_mobile' in params:
                work_mobile = (params.get('work_mobile'))
                log_vals.update({'mobile_phone': work_mobile or False})

            if 'work_phone' in params:
                work_phone = (params.get('work_phone'))
                log_vals.update({'work_phone': work_phone or False})

            if 'work_email' in params:
                work_email = (params.get('work_email'))
                log_vals.update({'work_email': work_email or False})

            if 'department' in params:
                department = (params.get('department'))
                log_vals.update({'department': department or False})

            if 'manager_id' in params:
                manager_id = int(params.get('manager_id'))
                log_vals.update({'manager_id': manager_id or False})

            if 'coach' in params:
                coach = int(params.get('coach'))
                log_vals.update({'coach_id': coach or False})

            if 'job_position' in params:
                job_position = (params.get('job_position'))
                log_vals.update({'job_position': job_position or False})

            if 'nationality' in params:
                nationality = int(params.get('nationality', False))
                log_vals.update({'nationality': nationality or False})

            if 'identification_number' in params:
                identification_number = (params.get('identification_number', False))
                log_vals.update({'identification_number': identification_number or False})

            if 'passport_number' in params:
                passport_number = (params.get('passport_number', False))
                log_vals.update({'passport_number': passport_number or False})

            if 'gender' in params:
                gender = (params.get('gender', False))
                log_vals.update({'gender': gender or False})

            if 'date_of_birth' in params:
                date_of_birth = (params.get('date_of_birth', False))
                log_vals.update({'birthday': date_of_birth or False})

            if 'place_of_birth' in params:
                place_of_birth = (params.get('place_of_birth', False))
                log_vals.update({'place_of_birth': place_of_birth or False})

            if 'country_of_birth' in params:
                country_of_birth = int(params.get('country_of_birth', False))
                log_vals.update({'country_of_birth': country_of_birth or False})

            if 'email' in params:
                email = (params.get('email', False))
                log_vals.update({'private_email': email or False})

            if 'phone' in params:
                phone = (params.get('phone', False))
                log_vals.update({'phone': phone or False})

            if 'marital_status' in params:
                marital_status = (params.get('marital_status', False))
                log_vals.update({'marital_status': marital_status or False})

            if 'aadhar_no' in params:
                aadhar_no = (params.get('aadhar_no', False))
                log_vals.update({'aadhar_no': aadhar_no or False})

            if 'identification_mark' in params:
                identification_mark = (params.get('identification_mark', False))
                log_vals.update({'identification_mark': identification_mark or False})

            if 'driving_licence_number' in params:
                driving_licence = (params.get('driving_licence_number', False))
                log_vals.update({'driving_licence': driving_licence or False})

            if 'driving_licence_validity' in params:
                driving_licence_validity = (params.get('driving_licence_validity', False))
                log_vals.update({'driving_licence_validity': driving_licence_validity or False})

            if 'driving_licence_attachment' in params:
                driving_licence_attachment = (params.get('driving_licence_attachment', False))
                log_vals.update({'driving_licence_attachment': driving_licence_attachment or False})

            if 'pan' in params:
                pan = (params.get('pan', False))
                log_vals.update({'pan': pan or False})

            if 'pan_validity' in params:
                pan_validity = (params.get('pan_validity', False))
                log_vals.update({'pan_validity': pan_validity or False})

            if 'pan_card_attachment' in params:
                pan_card_attachment = (params.get('pan_card_attachment ', False))
                log_vals.update({'pan_card_attachment': pan_card_attachment or False})

            if 'voter_id_number' in params:
                voter_id = (params.get('voter_id_number', False))
                log_vals.update({'voter_id': voter_id or False})

            if 'voter_id_validity' in params:
                voter_id_validity = (params.get('voter_id_validity', False))
                log_vals.update({'voter_id_validity': voter_id_validity or False})

            if 'voter_id_attachment' in params:
                voter_id_attachment = (params.get('voter_id_attachment ', False))
                log_vals.update({'voter_id_attachment': voter_id_attachment or False})

            if 'mines_certificate' in params:
                mines_certificate = (params.get('mines_certificate', False))
                log_vals.update({'mines_certificate': mines_certificate or False})

            if 'mines_certificate_validity' in params:
                mines_certificate_validity = (params.get('mines_certificate_validity', False))
                log_vals.update({'mines_certificate_validity': mines_certificate_validity or False})

            if 'mines_certificate_attachment' in params:
                mines_certificate_attachment = (params.get('mines_certificate_attachment', False))
                log_vals.update({'mines_certificate_attachment': mines_certificate_attachment or False})

            if 'emergency_contact' in params:
                emergency_contact = (params.get('emergency_contact', False))
                log_vals.update({'emergency_contact': emergency_contact or False})

            if 'emergency_phone' in params:
                emergency_phone = (params.get('emergency_phone', False))
                log_vals.update({'emergency_phone': emergency_phone or False})

            if 'badge_number' in params:
                badge_number = (params.get('badge_number', False))
                log_vals.update({'badge_number': badge_number or False})

            if 'photo' in params:
                photo = (params.get('photo', False))
                log_vals.update({'photo': photo or False})

            if 'religion' in params:
                religion = (params.get('religion', False))
                log_vals.update({'religion': religion or False})

            if 'language_lines' in params:
                language_lines = (params.get('language_lines', False))
                log_vals.update({'language_lines': language_lines or False})

            if 'experience' in params:
                experience = (params.get('experience', False))
                log_vals.update({'experience_line': experience or False})

            if 'tech_skill_lines' in params:
                skills = (params.get('tech_skills', False))
                log_vals.update({'tech_skills': skills or False})

            if 'address' in params:
                address = (params.get('address', False))
                log_vals.update({'address': address or False})

            if 'bank_details' in params:
                bank_details = (params.get('bank_details', False))
                log_vals.update({'bank_details': bank_details or False})

            if 'educational_qualification' in params:
                edu = (params.get('educational_qualification', False))
                log_vals.update({'educational_qualification': edu or False})

            if 'certification' in params:
                certificate = (params.get('certification', False))
                log_vals.update({'certificate': certificate or False})

            if 'pf_date' in params:
                pf_date = (params.get('pf_date', False))
                log_vals.update({'pf_date': pf_date or False})

            if 'uan_no' in params:
                uan_no = (params.get('uan_no', False))
                log_vals.update({'uan_no': uan_no or False})

            if 'nominee' in params:
                nominee = (params.get('nominee', False))
                log_vals.update({'nominee': nominee or False})

            if 'cpf' in params:
                cpf = (params.get('cpf', False))
                log_vals.update({'cpf': cpf or False})

            if 'lic_gratuity_no' in params:
                lic_gratuity_no = (params.get('lic_gratuity_no', False))
                log_vals.update({'lic_gratuity_no': lic_gratuity_no or False})

            if 'esi_applicable' in params:
                esi_applicable = (params.get('esi_applicable', False))
                log_vals.update({'esi_applicable': esi_applicable.lower() or False})

            if 'esi_no' in params:
                esi_no = (params.get('esi_no', False))
                log_vals.update({'esi_no': esi_no or False})

            if 'esi_join_date' in params:
                esi_join_date = (params.get('esi_join_date', False))
                log_vals.update({'esi_join_date': esi_join_date or False})

            if 'esi_last_date' in params:
                esi_last_date = (params.get('esi_last_date', False))
                log_vals.update({'esi_last_date': esi_last_date or False})

            if 'esi_exit_reason' in params:
                esi_exit_reason = (params.get('esi_exit_reason', False))
                log_vals.update({'esi_exit_reason': esi_exit_reason or False})

            if 'mines_wage_for_a_day' in params:
                mines_wage_for_a_day = (params.get('mines_wage_for_a_day', False))
                log_vals.update({'mines_wage_for_a_day': mines_wage_for_a_day or False})

            if 'mines_status' in params:
                mines_status = (params.get('mines_status', False))
                log_vals.update({'status': mines_status or False})

            if 'mines_gstin' in params:
                mines_gstin = (params.get('mines_gstin', False))
                log_vals.update({'gstin': mines_gstin or False})

            if 'mines_pf_retire_date' in params:
                mines_pf_retire_date = (params.get('mines_pf_retire_date', False))
                log_vals.update({'pf_retire_date': mines_pf_retire_date or False})

            if 'mines_basic_da' in params:
                mines_basic_da = (params.get('mines_basic_da', False))
                if mines_basic_da > 0:
                    log_vals.update({'basic_da': mines_basic_da or False})

            if 'mines_food_allowance' in params:
                mines_food_allowance = (params.get('mines_food_allowance', False))
                log_vals.update({'food_allowance': mines_food_allowance or False})

            if 'mines_other_allowance' in params:
                mines_other_allowance = (params.get('mines_other_allowance', False))
                log_vals.update({'other_allowance': mines_other_allowance or False})

            if 'mines_form_sl_no' in params:
                mines_form_sl_no = (params.get('mines_form_sl_no', False))
                log_vals.update({'mines_form_sl_no': mines_form_sl_no or False})

            if 'mines_working_unit' in params:
                mines_working_unit = (params.get('mines_working_unit', False))
                log_vals.update({'mines_working_unit': mines_working_unit or False})

            if 'mines_date_of_join_firm' in params:
                mines_date_of_join_firm = (params.get('mines_date_of_join_firm', False))
                log_vals.update({'mines_date_of_join_firm': mines_date_of_join_firm or False})

            if 'mines_classification' in params:
                mines_classification = (params.get('mines_classification', False))
                log_vals.update({'mines_classification': mines_classification or False})

            if 'labour_category' in params:
                labour_category = (params.get('labour_category', False))
                log_vals.update({'labour_category': labour_category or False})

            if 'pltn_labour_code' in params:
                pltn_labour_code = (params.get('pltn_labour_code', False))
                log_vals.update({'labour_code': pltn_labour_code or False})

            if 'pltn_division' in params:
                pltn_division = (params.get('pltn_division', False))
                log_vals.update({'division': pltn_division or False})

            if 'pltn_designation_group' in params:
                pltn_designation_group = (params.get('pltn_designation_group', False))
                log_vals.update({'designation_group': pltn_designation_group or False})

            if 'pltn_is_weekly_cash_payment' in params:
                pltn_is_weekly_cash_payment = (params.get('pltn_is_weekly_cash_payment', False))
                log_vals.update({'need_weekly_cash_payment': pltn_is_weekly_cash_payment.lower() or False})

            if 'pltn_from_date' in params:
                pltn_from_date = (params.get('pltn_from_date', False))
                log_vals.update({'from_date': pltn_from_date or False})

            if 'pltn_basic' in params:
                pltn_basic = (params.get('pltn_basic', False))
                if pltn_basic > 0:
                    log_vals.update({'basic': pltn_basic or False})

            if 'pltn_da' in params:
                pltn_da = (params.get('pltn_da', False))
                log_vals.update({'da': pltn_da or False})

            if 'pltn_ot_rate' in params:
                pltn_ot_rate = (params.get('pltn_ot_rate', False))
                log_vals.update({'ot_rate': pltn_ot_rate or False})

            if 'pltn_weightage' in params:
                pltn_weightage = (params.get('pltn_weightage', False))
                log_vals.update({'weightage': pltn_weightage or False})

            if 'pltn_pf_allotted' in params:
                pltn_pf_allotted = (params.get('pltn_pf_allotted', False))
                log_vals.update({'pf_allotted': pltn_pf_allotted.lower() or False})

            if 'pltn_pf_ac_no' in params:
                pltn_pf_ac_no = (params.get('pltn_pf_ac_no', False))
                log_vals.update({'pf_ac_no': pltn_pf_ac_no or False})

            if 'pltn_is_probation' in params:
                pltn_is_probation = (params.get('pltn_is_probation', False))
                log_vals.update({'probation': pltn_is_probation.lower() or False})

            if 'pltn_eligible_gratuity' in params:
                pltn_eligible_gratuity = (params.get('pltn_eligible_gratuity', False))
                log_vals.update({'eligible_gratuity': pltn_eligible_gratuity or False})

            if 'thumb_req' in params:
                thumb_req = (params.get('thumb_req', False))
                log_vals.update({'thumb_req': thumb_req.lower() or False})

            if 'in_and_out_req' in params:
                in_and_out_req = (params.get('in_and_out_req', False))
                log_vals.update({'in_and_out_req': in_and_out_req.lower() or False})

            if 'pltn_branch_name' in params:
                pltn_branch_name = (params.get('pltn_branch_name', False))
                log_vals.update({'branch_name': pltn_branch_name or False})

            if 'pltn_uniform_allotted' in params:
                pltn_uniform_allotted = (params.get('pltn_uniform_allotted', False))
                log_vals.update({'uniform_allotted': pltn_uniform_allotted.lower() or False})

            if 'pltn_leaving_date' in params:
                pltn_leaving_date = (params.get('pltn_leaving_date', False))
                log_vals.update({'leaving_date': pltn_leaving_date or False})

            if 'pltn_type_of_leave' in params:
                pltn_type_of_leave = (params.get('pltn_type_of_leave', False))
                log_vals.update({'type_of_leave': pltn_type_of_leave or False})

            if 'estate_name' in params:
                estate_name = (params.get('estate_name', False))
                log_vals.update({'estate_name': estate_name or False})

            if 'type' in params:
                type = (params.get('type', False))
                log_vals.update({'type': type or False})

            if 'residential_employee' in params:
                residential_employee = (params.get('residential_employee', False))
                log_vals.update({'residential_employee': residential_employee.lower() or False})

            if 'current_status' in params:
                current_status = (params.get('current_status', False))
                log_vals.update({'current_status': current_status.lower() or False})

            if 'retired' in params:
                retired = (params.get('retired', False))
                log_vals.update({'retired': retired.lower() or False})

            if 'mess_deduction' in params:
                mess_deduction = (params.get('mess_deduction', False))
                log_vals.update({'mess_deduction': mess_deduction.lower() or False})

            if 'show_in_payroll' in params:
                show_in_payroll = (params.get('show_in_payroll', False))
                log_vals.update({'show_in_payroll': show_in_payroll.lower() or False})

            if 'tds_required' in params:
                tds_required = (params.get('tds_required', False))
                log_vals.update({'tds_required': tds_required.lower() or False})

            if 'probation_start_date' in params:
                probation_start_date = (params.get('probation_start_date', False))
                log_vals.update({'probation_start_date': probation_start_date or False})

            if 'probation_end_date' in params:
                probation_end_date = (params.get('probation_end_date', False))
                log_vals.update({'probation_end_date': probation_end_date or False})

            if 'current_working_unit' in params:
                current_working_unit = (params.get('current_working_unit', False))
                log_vals.update({'current_working_unit': current_working_unit or False})

            if 'current_firm' in params:
                current_firm = (params.get('current_firm', False))
                log_vals.update({'current_firm': current_firm or False})

            if 'sub_firm' in params:
                sub_firm = (params.get('sub_firm', False))
                log_vals.update({'sub_firm': sub_firm or False})

            if 'grade' in params:
                grade = (params.get('grade', False))
                log_vals.update({'grade': grade or False})

            if 'production_incentive_designation' in params:
                production_incentive_designation = (params.get('production_incentive_designation', False))
                log_vals.update({'production_incentive_designation': production_incentive_designation or False})

            if 'leave_structure' in params:
                leave_structure = (params.get('leave_structure', False))
                log_vals.update({'leave_structure': leave_structure or False})

            if 'remarks' in params:
                remarks = (params.get('remarks', False))
                log_vals.update({'remarks': remarks or False})

            if 'mines_work_location' in params:
                mines_work_location = (params.get('mines_work_location', False))
                log_vals.update({'mines_work_location': mines_work_location or False})

            if 'mines_position' in params:
                mines_position = (params.get('mines_position', False))
                log_vals.update({'mines_position': mines_position or False})

            if 'mines_position_id' in params:
                mines_position_id = (params.get('mines_position_id', False))
                log_vals.update({'mines_position_id': mines_position_id or False})

            if 'exit_date' in params:
                exit_date = (params.get('exit_date', False))
                log_vals.update({'exit_date': exit_date or False})

            if 'work_location' in params:
                work_location = (params.get('work_location', False))
                log_vals.update({'work_location': work_location or False})

            if 'date_of_firm_join' in params:
                date_of_firm_join = (params.get('date_of_firm_join', False))
                log_vals.update({'date_of_firm_join': date_of_firm_join or False})

            if 'date_of_join' in params:
                date_of_join = (params.get('date_of_join', False))
                log_vals.update({'date_of_join': date_of_join or False})

            if 'contract_reference' in params:
                contract_reference = (params.get('contract_reference', False))
                log_vals.update({'contract_reference': contract_reference or False})

            if 'contract_start_date' in params:
                contract_start_date = (params.get('contract_start_date', False))
                log_vals.update({'contract_start_date': contract_start_date or False})

            if 'contract_end_date' in params:
                contract_end_date = (params.get('contract_end_date', False))
                log_vals.update({'contract_end_date': contract_end_date or False})

            if 'contract_state' in params:
                contract_state = (params.get('contract_state', False))
                log_vals.update({'contract_state': contract_state.lower() or False})

            if 'contract_notice_period' in params:
                contract_notice_period = int(params.get('contract_notice_period', False))
                log_vals.update({'contract_notice_period': contract_notice_period or False})

            if 'sal_struct_name' in params:
                sal_struct_name = (params.get('sal_struct_name', False))
                log_vals.update({'sal_struct_name': sal_struct_name or False})

            if 'sal_structure_reference' in params:
                sal_structure_reference = (params.get('sal_structure_reference', False))
                log_vals.update({'sal_structure_reference': sal_structure_reference or False})

            if 'salary_structure_type' in params:
                salary_structure_type = (params.get('salary_structure_type', False))
                log_vals.update({'salary_structure_type': salary_structure_type or False})

            if 'contract_salary_journal' in params:
                contract_salary_journal = int(params.get('contract_salary_journal', False))
                log_vals.update({'contract_salary_journal': contract_salary_journal or False})

            if 'Basic+DA' in params:
                basic_da = float(params.get('Basic+DA', False))
                log_vals.update({'wage': basic_da or False})

            if 'Basic' in params:
                basic_da = float(params.get('Basic', False))
                log_vals.update({'wage': basic_da or False})

            if 'T D S' in params:
                tds = float(params.get('T D S', False))
                log_vals.update({'tds': tds or False})

            if 'ROOM RENT' in params:
                room_rent = float(params.get('ROOM RENT', False))
                log_vals.update({'room_rent': room_rent or False})

            if 'Canteen Deduction' in params:
                canteen_deduction = float(params.get('Canteen Deduction', False))
                log_vals.update({'canteen_deduction': canteen_deduction or False})

            if 'HRA' in params:
                hra = float(params.get('HRA', False))
                log_vals.update({'hra': hra or False})

            if 'Phone Allowance' in params:
                phone_allowance = float(params.get('Phone Allowance', False))
                log_vals.update({'phone_allowance': phone_allowance or False})

            if 'Education Allowance' in params:
                education_allowance = float(params.get('Education Allowance', False))
                log_vals.update({'education_allowance': education_allowance or False})

            if 'Education Allowance(MAX)' in params:
                education_allowance_max = float(params.get('Education Allowance(MAX)', False))
                log_vals.update({'education_allowance_max': education_allowance_max or False})

            if 'Uniform Allowance' in params:
                uniform_allowance = float(params.get('Uniform Allowance', False))
                log_vals.update({'uniform_allowance': uniform_allowance or False})

            if 'Washing Allowance' in params:
                washing_allowance = float(params.get('Washing Allowance', False))
                log_vals.update({'washing_allowance': washing_allowance or False})

            if 'Food Allowance' in params:
                food_allowance = float(params.get('Food Allowance', False))
                log_vals.update({'meal_allowance': food_allowance or False})

            if 'LTA(MAX)' in params:
                lta_max = float(params.get('LTA(MAX)', False))
                log_vals.update({'lta_max': lta_max or False})

            if 'Servant Allowance' in params:
                servant_allowance = float(params.get('Servant Allowance', False))
                log_vals.update({'servant_allowance': servant_allowance or False})

            if 'Conveyance Allowance' in params:
                conveyance_allowance = float(params.get('Conveyance Allowance', False))
                log_vals.update({'conveyance_allowance': conveyance_allowance or False})

            if 'Special Allowance' in params:
                special_allowance = float(params.get('Special Allowance', False))
                log_vals.update({'special_allowance': special_allowance or False})

            if 'Plantation Allowance' in params:
                plantation_allowance = float(params.get('Plantation Allowance', False))
                log_vals.update({'plantation_allowance': plantation_allowance or False})

            if 'Composite Allowance' in params:
                composite_allowance = float(params.get('Composite Allowance', False))
                log_vals.update({'composite_allowance': composite_allowance or False})

            if 'Petrol Allowance' in params:
                petrol_allowance = float(params.get('Petrol Allowance', False))
                log_vals.update({'petrol_allowance': petrol_allowance or False})

            if 'Daily Allowance' in params:
                daily_allowance = float(params.get('Daily Allowance', False))
                log_vals.update({'daily_allowance': daily_allowance or False})

            if 'Kit Allowance(MAX)' in params:
                kit_allowance = float(params.get('Kit Allowance(MAX)', False))
                log_vals.update({'kit_allowance': kit_allowance or False})

            if 'wage_type' in params:
                wage_type = (params.get('wage_type', False))
                log_vals.update({'wage_type': wage_type.lower() or False})

            if 'hr_responsible_id' in params:
                hr_responsible_id = int(params.get('hr_responsible_id', False))
                log_vals.update({'hr_responsible_id': hr_responsible_id or False})

            if 'salary_structure_id' in params:
                salary_structure_id = int(params.get('salary_structure_id', False))
                log_vals.update({'salary_structure_id': salary_structure_id or False})

            if 'salary_advantage' in params:
                salary_advantage_details = (params.get('salary_advantage', False))
                log_vals.update({'salary_advantage_details': salary_advantage_details or False})

            if 'salary_deduction' in params:
                salary_deduction_details = (params.get('salary_deduction', False))
                log_vals.update({'salary_deduction_details': salary_deduction_details or False})

            if 'emp_history' in params:
                emp_history = (params.get('emp_history', False))
                log_vals.update({'emp_history': emp_history or False})

            if 'Salary_hike' in params:
                Salary_hike = (params.get('Salary_hike', False))
                log_vals.update({'Salary_hike': Salary_hike or False})

            if 'company_id' in params:
                company_id = int(params.get('company_id', False))
                log_vals.update({'company_id': company_id or False})
            else:
                _logger.info('Service API : Company ID Not Available Returning')
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred - Company ID Not Available",
                })

            if params['username'] and params['password']:
                server_url = 'http://localhost:8069'
                try:

                    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(server_url))
                    response = models.execute_kw(request.env.cr.dbname, user_id.id, str(params['password']),
                                                 'employee.api.create',
                                                 'action_create_employee', [log_vals])
                    employee_dict = json.loads(response)  # converted

                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': employee_dict['status'],
                        'status_code': employee_dict['status_code'],
                        'employee_id': employee_dict['employee_id']

                    })
                except Exception as e:
                    status = "REJECTED"
                    status_code = 500
                    _logger.info("Service API : Error %s", e)
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'msg': "Error : " + str(e),
                    })
            else:
                status = "REJECTED"
                status_code = 401
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'msg': "An Error Occurred",
                })


        else:
            status = "REJECTED"
            status_code = 500
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'msg': "Params Not Available",
            })
