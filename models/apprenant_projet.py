# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
#from datetime import  datetime

class apprenant_projet(models.Model):
    _name = "apprenant.projet"
    _description = "Projets des apprenants au CAFRAD"
    _rec_name = 'name'
    _order = 'id DESC'

    @api.model
    def _get_default_academic_year(self):
        academic_year_obj = self.env['ane.academiq.cafrad']
        academic_year_id = academic_year_obj.search([('actived', '=', True)], limit=1)
        return academic_year_id and academic_year_id.id or False

    name = fields.Char("Nom du projet", required=1)
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Année Académique",
                                        default=lambda self: self._get_default_academic_year(), required=True)

    date_register = fields.Datetime('Date d\'énregistrement', default=fields.datetime.now(), readonly=1)
    objectif= fields.Text("Objectifs")
    moyens = fields.Text("Moyens Necessaires")
    observation = fields.Text("Observations")
    day_hour = fields.Text("JOUR/HEURE")
    # date_start = fields.Date('Date de debut', default=datetime.today().date())
    # date_end = fields.Date('Date de fin')
    # hour_start = fields.Datetime('Heure de debut')
    # hour_end = fields.Datetime("Heure de fin")



class apprenant_suivi_projet(models.Model):
    _name = "apprenant.suivi.projet"
    _description = "Suivi des projets au CAFRAD"
    _rec_name = 'name'
    _order = 'id DESC'

    @api.model
    def _get_default_academic_year(self):
        academic_year_obj = self.env['ane.academiq.cafrad']
        academic_year_id = academic_year_obj.search([('actived', '=', True)], limit=1)
        return academic_year_id and academic_year_id.id or False

    name = fields.Char("Description", required=1)
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Année Académique",
                                        default=lambda self: self._get_default_academic_year(), required=True)
    date_register = fields.Datetime('Date d\'énregistrement', default=fields.datetime.now(), readonly=1)
    apprenant_id = fields.Many2one('apprenant.cafrad',string="Apprenant")
    reponsable_id = fields.Many2one('hr.employee', "Responsable du suivi",
                                    help="Il s'agit du personel en charge du suivi du projet de l'apprenant")
    projet_id = fields.Many2one('apprenant.projet', string="Activités/Projets")

    lines_suivi_projet_ids = fields.One2many('apprenant.suivi.projet.line', 'suivi_projet_id',
                                            string='Lignes de suivi de Projets')


class apprenant_suivi_projet_line(models.Model):
    _name = "apprenant.suivi.projet.line"
    _description = "Lignes de suivi des projets au CAFRAD"

    _order = 'id DESC'

    date_register = fields.Datetime('Date d\'énregistrement', default=fields.datetime.now())
    action = fields.Char("Actions menées")
    resultat = fields.Char("Resultats Obtenus")
    difficulte = fields.Char("Resultats Obtenus")
    solution = fields.Char("Solutions Devellopées/Envisagées")
    suivi_projet_id = fields.Many2one('apprenant.suivi.projet', string="Projet")

