# -*- coding: utf-8 -*-
# from odoo import http


# class CafradApp(http.Controller):
#     @http.route('/cafrad_app/cafrad_app/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cafrad_app/cafrad_app/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cafrad_app.listing', {
#             'root': '/cafrad_app/cafrad_app',
#             'objects': http.request.env['cafrad_app.cafrad_app'].search([]),
#         })

#     @http.route('/cafrad_app/cafrad_app/objects/<model("cafrad_app.cafrad_app"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cafrad_app.object', {
#             'object': obj
#         })
