import json
import logging
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)



class ContractTemplateCreateAPI(models.Model):
    _name = 'contract_template.api.create'


    @api.model
    def action_create_contract_template(self, vals):

        contractadvantage_vals = {}
        contractdeduction_vals = {}

        if 'name' in vals:
            name = (vals.get('name'))
            contractadvantage_vals.update({'name': name})
            contractdeduction_vals.update({'name': name})

        # contractadvantage_vals.update({'code': vals.get('name')[0:4].upper()})
        # contractdeduction_vals.update({'code': vals.get('name')[0:4].upper()})

        if 'calc_based_on' in vals:
            periodicity = (vals.get('calc_based_on'))
            if periodicity == 'I':
                contractadvantage_vals.update({'periodicity': 'yearly'})
            else:
                contractadvantage_vals.update({'periodicity': 'monthly'})

        global calc_global
        calc_global = (vals.get('calcflag'))
        calc_flag = (vals.get('calcflag'))
        if calc_flag == 'D':
            code = self.code_genarator(vals.get('name')[0:4].upper())
            contractdeduction_vals.update({'code': code})
            contract_deduction_check = self.env['hr.contract.deduction.template'].search(
                [('name', '=', vals.get('name'))])
            if contract_deduction_check:
                contract_deduction = contract_deduction_check
                _logger.info("Service API : Contract Already Deduction Created")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'contract_deduction': contract_deduction.id,
                    'contract_advantage': 0
                })
            else:
                contract_deduction = self.env['hr.contract.deduction.template'].create(contractdeduction_vals)
                if contract_deduction:
                    _logger.info("Service API : Contract Deduction Created")
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'contract_deduction': contract_deduction.id,
                        'contract_advantage': 0
                    })
                else:
                    _logger.info("Service API : Contract Deduction Creation Failed")
                    status = 'REJECTED'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'contract_deduction': contract_deduction.id,
                        'contract_advantage': 0
                    })

        elif calc_flag == 'A':
            code = self.code_genarator(vals.get('name')[0:4].upper())
            contractadvantage_vals.update({'code': code})
            contract_advantage_check = self.env['hr.contract.advantage.template'].search(
                [('name', '=', vals.get('name')), ('periodicity', '=', contractadvantage_vals.get('periodicity'))])
            if contract_advantage_check:
                contract_advantage = contract_advantage_check
                _logger.info("Service API : Contract Advantage Already Created")
                status = 'SUCCESS'
                status_code = 200
                return json.dumps({
                    'status': status,
                    'status_code': status_code,
                    'contract_advantage': contract_advantage.id,
                    'contract_deduction': 0
                })
            else:
                contract_advantage = self.env['hr.contract.advantage.template'].create(contractadvantage_vals)
                if contract_advantage:
                    _logger.info("Service API : Contract Advantage Created")
                    status = 'SUCCESS'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'contract_advantage': contract_advantage.id,
                        'contract_deduction': 0
                    })
                else:
                    _logger.info("Service API : Contract Advantage Creation Failed")
                    status = 'REJECTED'
                    status_code = 200
                    return json.dumps({
                        'status': status,
                        'status_code': status_code,
                        'contract_advantage': contract_advantage.id,
                        'contract_deduction': 0
                    })

    def code_genarator(self, code):
        final_code = ''
        code_search = self.code_search(code)
        if calc_global == 'A':
            code_search_advantage = self.env['hr.contract.advantage.template'].search([("code", "=", code_search)])
            if code_search_advantage:
                final_code = self.code_search(code_search)
            else:
                final_code = code_search
        if calc_global == 'D':
            code_search_deduction = self.env['hr.contract.deduction.template'].search([("code", "=", code_search)])
            if code_search_deduction:
                final_code = self.code_search(code_search)
            else:
                final_code = code_search
        return final_code

    def code_search(self, code):
        n = "1"
        code_generated = ''
        code_bool = False
        if calc_global == 'A':
            code_search_advantage = self.env['hr.contract.advantage.template'].search([("code", "=", code)])
            if code_search_advantage:
                code_bool = True
            else:
                code_generated = code
            while code_bool:
                t = ""
                for i in code:
                    if (i.isdigit()):
                        n += i
                    else:
                        t += i
                num = int(n)
                code_while = t + str(num)
                code_search_advantage = self.env['hr.contract.advantage.template'].search([("code", "=", code_while)])
                if code_search_advantage:
                    n = str(num + 1)
                else:
                    code_generated = code_while
                    code_bool = False
        if calc_global == 'D':
            code_search_deduction = self.env['hr.contract.deduction.template'].search([("code", "=", code)])
            if code_search_deduction:
                code_bool = True
            else:
                code_generated = code
            while code_bool:
                t = ""
                for i in code:
                    if (i.isdigit()):
                        n += i
                    else:
                        t += i
                num = int(n)
                code_while = t + str(num)
                code_search_deduction = self.env['hr.contract.deduction.template'].search([("code", "=", code_while)])
                if code_search_deduction:
                    n = str(num + 1)
                else:
                    code_generated = code_while
                    code_bool = False
        return code_generated


class SalaryStructureCreateAPI(models.Model):
    _name = 'salary_structure.api.create'

    @api.model
    def action_create_salary_structure(self, vals):

        salary_structure_vals = {}

        if 'name' in vals:
            name = (vals.get('name'))
            salary_structure_vals.update({'name': name})

        if 'contract_deduction' in vals:
            contract_deduction_ids = []
            contract_string = vals['contract_deduction']
            if contract_string:
                contract_list = contract_string.split(',')
                for contract_id in contract_list:
                    contract_deduction_ids.append(int(contract_id))
                salary_structure_vals.update({'contract_deduction_ids': [(6, 0, contract_deduction_ids or [])]})

        if 'contract_advantage' in vals:
            contract_ids = []
            contract_string = vals['contract_advantage']
            if contract_string:
                contract_list = contract_string.split(',')
                for contract_id in contract_list:
                    contract_ids.append(int(contract_id))
                salary_structure_vals.update({'contract_advantages_ids': [(6, 0, contract_ids or [])]})

        salary_structure = self.env['hr.payroll.structure'].create(salary_structure_vals)

        if salary_structure:
            _logger.info("Service API : Salary Structure Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'salary_structure': salary_structure.id,
            })
        else:
            _logger.info("Service API : Salary Structure Creation Failed")
            status = 'REJECTED'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'salary_structure': salary_structure.id
            })
