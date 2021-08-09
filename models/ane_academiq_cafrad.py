# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class ane_academiq_cafrad(models.Model):
    _name = "ane.academiq.cafrad"
    _description = "Annee Academique au CAFRAD"
    _order = 'id DESC'


    date_start = fields.Date('Date de debut', required=True)
    date_end = fields.Date('Date de fin', required=True)
    active = fields.Boolean('Actif?', default=False)

    def name_get(self):
        res = []
        for r in self:
            final_name = "%s - %s" % (r.date_start, r.date_end)
            res.append(tuple([r.id, final_name]))
        return res
