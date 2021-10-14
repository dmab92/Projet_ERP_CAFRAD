# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _

class anne_academiq_cafrad(models.Model):
    _name = "ane.academiq.cafrad"
    _description = "Annee Academique au CAFRAD"
    _order = 'id DESC'


    date_start = fields.Date('Date de debut', required=True)
    date_end = fields.Date('Date de fin', required=True)
    actived = fields.Boolean('Active ?')
    description = fields.Char("Description")
    next_academique_id = fields.Many2one('ane.academiq.cafrad', 'Année Academique Suivante',
                                        help="Selectionnée l'Année Academique Suivante")

    def name_get(self):
        '''Method to display name and code'''
        return [(rec.id, ' ' + str(rec.date_start.year) + '/' + str(rec.date_end.year)) for rec in self]
