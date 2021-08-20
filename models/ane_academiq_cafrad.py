# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class ane_academiq_cafrad(models.Model):
    _name = "ane.academiq.cafrad"
    _description = "Annee Academique au CAFRAD"
    _order = 'id DESC'

    date_start = fields.Date('Date de debut', required=True)
    date_end = fields.Date('Date de fin', required=True)
    active = fields.Boolean('Active?', default=False)
    description = fields.Char("Description")
    next_academique_id = fields.Many2one('ane.academiq.cafrad', 'Année Academique Suivante',
                                        help="Selectionnée l'Année Academique Suivante")

    # def name_get(self):
    #     res = []
    #     for r in self:
    #         final_name = "%s - %s" % (r.date_start, r.date_end)
    #         res.append(tuple([r.id, final_name]))
    #     return res

    def name_get(self):
        '''Method to display name and code'''
        return [(rec.id, ' ' + str(rec.date_start.year) + '/' + str(rec.date_end.year)) for rec in self]
