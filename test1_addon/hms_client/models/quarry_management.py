import json
import logging
import pytz
import datetime
from decimal import Decimal
from odoo import _, api, fields, models
from odoo.exceptions import UserError

from datetime import datetime

_logger = logging.getLogger(__name__)


class QuarryGeneralWorkCreateAPI(models.Model):
    _name = 'quarry_work.api.create'

    @api.model
    def action_create_quarry_general_work(self, values):

        quarry_work_vals = {}


        if 'name' in values:
            name = values.get('name', False)
            quarry_work_vals.update({'name': name or False})

        if 'date' in values:
            date = values.get('date', False)
            quarry_work_vals.update({'date': date or False})

        if 'quarry' in values:
            quarry = int(values.get('quarry', False))
            quarry_work_vals.update({'quarry': quarry or False})

        if 'work_head_id' in values:
            work_head_id = int(values.get('work_head_id', False))
            quarry_work_vals.update({'work_head_id': work_head_id or False})

        if 'sub_contractor' in values:
            sub_contractor = int(values.get('sub_contractor', False))
            quarry_work_vals.update({'sub_contractor': sub_contractor or False})

        if 'particulars' in values:
            particulars = values.get('particulars', False)
            quarry_work_vals.update({'particulars': particulars or False})

        if 'amount' in values:
            amount = float(values.get('amount', False))
            quarry_work_vals.update({'amount': amount or False})

        if 'space' in values:
            space = values.get('space', False)
            quarry_work_vals.update({'space': space or False})

        quarry_general_work_id = self.env['quarry.general.works'].create(quarry_work_vals)
        if quarry_general_work_id:
            _logger.info("Service API : Quarry General Work Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'quarry_general_work_id': quarry_general_work_id.id,
            })


class DrillingCreateAPI(models.Model):
    _name = 'drilling.api.create'

    @api.model
    def action_create_drilling(self, values):

        drilling_vals = {}


        if 'name' in values:
            name = values.get('name', False)
            drilling_vals.update({'name': name or False})

        if 'date' in values:
            date = values.get('date', False)
            drilling_vals.update({'date': date or False})

        if 'quarry' in values:
            quarry = int(values.get('quarry', False))
            drilling_vals.update({'quarry': quarry or False})

        if 'type_of_drilling' in values:
            type_of_drilling = values.get('type_of_drilling', False)
            drilling_vals.update({'type_of_drilling': type_of_drilling or False})

        if 'compressor' in values:
            compressor = values.get('compressor', False)
            drilling_vals.update({'compressor': compressor or False})

        if 'jack_hammer_id' in values:
            jack_hammer_id = int(values.get('jack_hammer_id', False))
            drilling_vals.update({'jack_hammer_id': jack_hammer_id or False})

        if 'jack_hammer_working' in values:
            jack_hammer_working = float(values.get('jack_hammer_working', False))
            drilling_vals.update({'jack_hammer_working': jack_hammer_working or False})

        if 'drill_bit' in values:
            drill_bit = values.get('drill_bit', False)
            drilling_vals.update({'drill_bit': drill_bit or False})

        if 'hole_sizes' in values:
            hole_sizes = values.get('hole_sizes')
            hole_size_inc = 0
            hole_size_det = []

            for hole_size in hole_sizes:
                hole_size_data = {}
                hole_size_data.update({'hole_size': str(hole_size['hole_size'])})
                hole_size_data.update({'feets_drilled': float(hole_size['feets_drilled'])})

                hole_size_det.append((0, hole_size_inc, hole_size_data))
                hole_size_inc = hole_size_inc + 1
            _logger.info("Service API :Drilling Details (%s)", hole_size_det)
            drilling_vals.update({"feets_drilled_ids": hole_size_det})

        drilling_id = self.env['drilling.work'].create(drilling_vals)
        if drilling_id:
            _logger.info("Service API : Drilling Work Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'drilling_id': drilling_id.id,
            })


class BlastingCreateAPI(models.Model):
    _name = 'blasting.api.create'

    @api.model
    def action_create_blasting(self, values):

        blasting_vals = {}

        if 'name' in values:
            name = values.get('name', False)
            blasting_vals.update({'name': name or False})

        if 'date' in values:
            date = values.get('date', False)
            blasting_vals.update({'date': date or False})

        if 'quarry' in values:
            quarry = int(values.get('quarry', False))
            blasting_vals.update({'quarry': quarry or False})

        if 'type_of_blasting' in values:
            type_of_blasting = values.get('type_of_blasting', False)
            blasting_vals.update({'type_of_blasting': type_of_blasting or False})

        if 'labour_details' in values:
            labour_details = values.get('labour_details')
            labour_count = 0
            labour_det = []

            for details in labour_details:
                labour_data = {}
                labour_data.update({'amount': float(details['amount'])})
                labour_data.update({'labour_id': int(details['labour_id'])})

                labour_det.append((0, labour_count, labour_data))
                labour_count = labour_count + 1
            _logger.info("Service API :Labour Details (%s)", labour_det)
            blasting_vals.update({"labour_ids": labour_det})

        if 'drill_hole_details' in values:
            drill_hole_details = values.get('drill_hole_details')
            drill_count = 0
            drill_hole_det = []

            for details in drill_hole_details:
                drill_hole_data = {}
                drill_hole_data.update({'no_of_holes': int(details['no_of_holes'])})
                drill_hole_data.update({'hole_size': str(details['hole_size'])})

                drill_hole_det.append((0, drill_count, drill_hole_data))
                drill_count = drill_count + 1
            _logger.info("Service API :Drill Hole Details (%s)", drill_hole_det)
            blasting_vals.update({"hole_size_ids": drill_hole_det})

        blasting_id = self.env['blasting.work'].create(blasting_vals)
        if blasting_id:
            _logger.info("Service API : Blasting Work Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'blasting_id': blasting_id.id,
            })



class QuarryCreateAPI(models.Model):
    _name = 'quarry.api.create'

    @api.model
    def action_create_quarry(self, values):

        event_type = ''
        quarry_vals = {}

        if 'event_type' in values:
            event_type = values.get('event_type')

        if 'quarry_name' in values:
            quarry_name = values.get('quarry_name', False)
            quarry_vals.update({'quarry_name': quarry_name or False})

        if 'area' in values:
            area = values.get('area', False)
            quarry_vals.update({'area': area or False})

        if 'village' in values:
            village = values.get('village', False)
            quarry_vals.update({'village': village or False})

        if 'taluk' in values:
            taluk = values.get('taluk', False)
            quarry_vals.update({'taluk': taluk or False})

        if 'district' in values:
            district = values.get('district', False)
            quarry_vals.update({'district': district or False})

        if 'estimated_output' in values:
            estimated_output = values.get('estimated_output', False)
            quarry_vals.update({'estimated_output': estimated_output or False})

        if 'run_time_to_plant' in values:
            run_time_to_plant = float(values.get('run_time_to_plant', False))
            quarry_vals.update({'run_time_to_plant': run_time_to_plant or False})

        if 'rent' in values:
            rent = float(values.get('rent', False))
            quarry_vals.update({'rent': rent or False})

        if 'distance_from_plant' in values:
            distance_from_plant = float(values.get('distance_from_plant', False))
            quarry_vals.update({'distance_from_plant': distance_from_plant or False})

        if 'state_id' in values:
            state_id = int(values.get('state_id', False))
            quarry_vals.update({'state_id': state_id or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            quarry_vals.update({'company_id': company_id or False})

        quarry_id = self.env['chart.of.quarry'].create(quarry_vals)
        if quarry_id:
            _logger.info("Service API : Quarry Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'quarry_id': quarry_id.id,
            })


class MiningCreateAPI(models.Model):
    _name = 'mining.api.create'

    @api.model
    def action_create_mining(self, values):

        mining_vals = {}


        if 'name' in values:
            name = values.get('name', False)
            mining_vals.update({'name': name or False})

        if 'belongs_to' in values:
            belongs_to = values.get('belongs_to', False)
            mining_vals.update({'belongs_to': belongs_to or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            mining_vals.update({'company_id': company_id or False})

        mining_id = self.env['chart.of.mining.works'].create(mining_vals)
        if mining_id:
            _logger.info("Service API : Mining Works Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'mining_id': mining_id.id,
            })

class JackhammerCreateAPI(models.Model):
    _name = 'jackhammer.api.create'

    @api.model
    def action_create_jackhammer(self, values):

        jackhammer_vals = {}


        if 'jack_hammer' in values:
            jack_hammer = values.get('jack_hammer', False)
            jackhammer_vals.update({'jack_hammer': jack_hammer or False})

        if 'asset_id' in values:
            asset_id = values.get('asset_id', False)
            jackhammer_vals.update({'asset_id': asset_id or False})

        if 'company_id' in values:
            company_id = int(values.get('company_id', False))
            jackhammer_vals.update({'company_id': company_id or False})

        jackhammer_id = self.env['chart.of.jackhammer'].create(jackhammer_vals)
        if jackhammer_id:
            _logger.info("Service API : JackHammer Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'jackhammer_id': jackhammer_id.id,
            })


class MiningCreateAPI(models.Model):
    _name = 'explosive_consumption_marking.api.create'

    @api.model
    def action_create_explosive_consumption(self, values):

        explosive_consumption_vals = {}

        if 'blaster' in values:
            blaster = values.get('blaster', False)
            explosive_consumption_vals.update({'blaster': blaster or False})

        if 'date' in values:
            date = values.get('date', False)
            explosive_consumption_vals.update({'date': date or False})

        if 'material_items' in values:
            material_items = values.get('material_items')
            material_pos = 0
            material_item_det = []

            for material_request_item in material_items:
                material_item_data = {}
                material_item_data.update({'material': str(material_request_item['material'])})
                material_item_data.update({'overburden': float(material_request_item['overburden'])})
                material_item_data.update({'primary': float(material_request_item['primary'])})
                material_item_data.update({'secondary': float(material_request_item['secondary'])})
                material_item_data.update({'total': float(material_request_item['total'])})

                material_item_det.append((0, material_pos, material_item_data))
                material_pos = material_pos + 1
            _logger.info("Service API :Material Details (%s)", material_item_det)
            explosive_consumption_vals.update({"material_ids": material_item_det})

        explosive_consumption_id = self.env['explosive.consumption.marking'].create(explosive_consumption_vals)
        if explosive_consumption_id:
            _logger.info("Service API : Explosive Consumption Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'explosive_consumption_id': explosive_consumption_id.id,
            })


class MiningCreateAPI(models.Model):
    _name = 'e_filling.api.create'

    @api.model
    def action_create_e_filling(self, values):

        e_filling_vals = {}

        if 'date' in values:
            date = values.get('date', False)
            e_filling_vals.update({'date': date or False})

        if 'time' in values:
            time = values.get('time', False)
            e_filling_vals.update({'time': time or False})

        if 'remarks' in values:
            remarks = values.get('remarks', False)
            e_filling_vals.update({'remarks': remarks or False})

        if 'employee_id' in values:
            employee_id = int(values.get('employee_id', False))
            e_filling_vals.update({'employee_id': employee_id or False})

        e_filling_id = self.env['e.filling.entry'].create(e_filling_vals)
        if e_filling_id:
            _logger.info("Service API : Explosive Daily e-Filling Entry Created")
            status = 'SUCCESS'
            status_code = 200
            return json.dumps({
                'status': status,
                'status_code': status_code,
                'e_filling_id': e_filling_id.id,
            })