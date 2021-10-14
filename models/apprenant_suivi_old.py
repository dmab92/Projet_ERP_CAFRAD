# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError

class apprenant_cafrad_suivi(models.Model):
    _name = "apprenant.cafrad.suivi"
    _description = "Suivi des apprenannts du CAFRAD"
    _order = 'id DESC'

    @api.model
    def _get_default_responsable_suivi(self):
        employee_obj = self.env['hr.employee']
        reponsable_id = employee_obj.search([('user_id', '=', self.env.uid)], limit=1)
        return reponsable_id and reponsable_id.id or False

    apprenant_id = fields.Many2one('apprenant.cafrad',string="Nom du Jeune", required=True,
                                   domain=[('ane_academique_id.active','=',True)])

    apprenant_phone = fields.Char("Téléphone de l'apprenant")

    ane_academique_id = fields.Many2one('ane.academiq.cafrad', 'Année Academique',
                                        help="Selection l'Année Academique")
    class_room_id = fields.Many2one('salle.classe.cafrad',string='Salle de Classe', help="La classe de l'apprenant")
    reponsable_id = fields.Many2one('hr.employee', "Responsable du suivi", required='1',
                                    default=lambda self: self._get_default_responsable_suivi(),
                                    help="Il s'agit du personel en charge du suivi de l'apprnant")



    fiche_suivi_line_ids = fields.One2many("apprenant.cafrad.suivi.fiche.line",
                                           'apprenant_suivi_fiche_id',string="Suivi de l'apprenant")

    @api.onchange('apprenant_id')
    def _onchange_apprenant_id(self):
        for rec in self:
            if rec.apprenant_id:
                rec.ane_academique_id = rec.apprenant_id.ane_academique_id
                rec.class_room_id = rec.apprenant_id.classe_id
                rec.apprenant_phone= rec.apprenant_id.apprenant_phone





    def set_to_running(self):
         for record in self:
             if record.state_suivi not in ['draft']:
                 raise UserError(_("Alerte !!! pour faire passer le suivi cet "
                                   "apprenant en cours d'insertion, il doit etre en brouiilon"))
         return self.write({"state_suivi": 'running'})

    def set_to_insert(self):
        for record in self:
            if record.state_suivi not in ['running']:
                raise UserError(_("Alerte !!! pour faire passer le suivi cet "
                                  "apprenant a insertion a dans une entreprise, "
                                  "rassurer vous qu'il soit d'abord en cours d'insertion"))

        return self.write({"state_suivi": 'insert'})

    def set_to_insertalone(self):
        for record in self:
            if record.state_suivi not in ['running']:
                raise UserError(_("Alerte !!! pour faire passer le suivi cet "
                                  "apprenant a insertion a son compte, "
                                  "rassurer vous qu'il soit d'abord en cours d'insertion"))
        return self.write({"state_suivi": 'insertalone'})

    def set_to_draft(self):
        for record in self :
            if record.state_suivi == 'draft':
                raise UserError(_("Alerte !!!  vous voulez mettre en brouillon, "
                                  "le suivi d'un apprenant qui est deja en brouillon"))
        return self.write({"state_suivi": 'draft'})

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






