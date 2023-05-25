# -*- coding: utf-8 -*-
# from odoo import http


# class TaxCollectionAtSource(http.Controller):
#     @http.route('/tax_collection_at_source/tax_collection_at_source/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tax_collection_at_source/tax_collection_at_source/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tax_collection_at_source.listing', {
#             'root': '/tax_collection_at_source/tax_collection_at_source',
#             'objects': http.request.env['tax_collection_at_source.tax_collection_at_source'].search([]),
#         })

#     @http.route('/tax_collection_at_source/tax_collection_at_source/objects/<model("tax_collection_at_source.tax_collection_at_source"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tax_collection_at_source.object', {
#             'object': obj
#         })
