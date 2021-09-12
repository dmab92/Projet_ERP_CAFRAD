# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class apprenant_cafrad_suivi(models.Model):
    _name = "apprenant.cafrad.suivi"
    _description = "Suivi des apprenannts du CAFRAD"
    _order = 'id DESC'


    apprenant_id = fields.Many2one('apprenant.cafrad',string="Nom du Jeune", required=True,
                                   domain=[('ane_academique_id.active','=',True)])

    apprenant_phone = fields.Char("Téléphone de l'apprenant")

    ane_academique_id = fields.Many2one('ane.academiq.cafrad', 'Année Academique',
                                        help="Selection l'Année Academique")
    class_room_id = fields.Many2one('salle.classe.cafrad',string='Salle de Classe', help="La classe de l'apprenant")
    reponsable_id = fields.Many2one('hr.employee', "Responsable du suivi",
                                    help="Il s'agit du personel en charge du suivi de l'apprnant")



    fiche_suivi_line_ids = fields.One2many("apprenant.cafrad.suivi.fiche.line",'apprenant_suivi_fiche_id',string="Suivi de l'apprenant")

    @api.onchange('apprenant_id')
    def _onchange_apprenant_id(self):
        for rec in self:
            if rec.apprenant_id:
                rec.ane_academique_id = rec.apprenant_id.ane_academique_id
                rec.class_room_id = rec.apprenant_id.classe_id
                rec.apprenant_phone= rec.apprenant_id.apprenant_phone


    def print_fiche_suivi(self):
        # datas = {
        #
        # }
        return self.env.ref('cafrad_app.action_report_fiche_suivi').report_action(self)





class apprenant_cafrad_suivi_line(models.Model):
    _name = "apprenant.cafrad.suivi.fiche.line"
    _description = "Line de Suivi des apprenannts du CAFRAD"
    _order = 'id DESC'

    date_suivi = fields.Datetime('Jour/H de sivi', default=fields.datetime.now())
    visit_or_call = fields.Selection([('visit', 'Visite'), ('call', 'Appel')], 'Visite ou  Appel')
    activity = fields.Text(string="Activités")
    person_call=  fields.Char("Qui avez vous rencontrer ou appelé?")
    activi_evolution = fields.Char("Evolution de l'activité ?")
    difficulty= fields.Char('Difficicultés Rencontrées')
    solution = fields.Char("Solution envisagée/Obsevation")
    date_rdv = fields.Datetime('Prochain Rdv')
    apprenant_suivi_fiche_id = fields.Many2one('apprenant.cafrad.suivi.fiche')






