#-*- coding: utf-8 -*-

from odoo import models, fields, api


class tdb_cafrad(models.Model):
    _name = 'tdb_cafrad.cafrad'
    _description = 'Tableau de bord Special du manager'

    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Annee Academique",
                                        default=lambda self: self._get_default_academic_year())
    total_apprenant = fields.Char("Nombre Total d'apprenants")
    total_prospect = fields.Char("Nombre Total d'apprenants")
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    #type="measure" 
    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
