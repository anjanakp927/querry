# -*- coding: utf-8 -*-
# from odoo import http


# class BuildingAnj(http.Controller):
#     @http.route('/building_anj/building_anj/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/building_anj/building_anj/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('building_anj.listing', {
#             'root': '/building_anj/building_anj',
#             'objects': http.request.env['building_anj.building_anj'].search([]),
#         })

#     @http.route('/building_anj/building_anj/objects/<model("building_anj.building_anj"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('building_anj.object', {
#             'object': obj
#         })
