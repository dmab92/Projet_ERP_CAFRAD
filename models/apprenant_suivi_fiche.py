# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError

class apprenant_cafrad_suivi_fiche(models.Model):
    _name = "apprenant.cafrad.suivi.fiche"
    _description = "Fiche de Suivi des apprenannts du CAFRAD"
    _order = 'id DESC'
    _rec_name = 'apprenant_id'

    state = fields.Selection([('draft', 'En attente d''insertion'),
                              ('running', 'En cours d''insertion'),
                              ('insert', 'Inseré(e)')], default='draft')
    ################################## A/-ACCOMPAGNEMENT SOCIAL  ########################################

    apprenant_id = fields.Many2one('apprenant.cafrad',string="Nom du Jeune", required=True,
                                   domain=[('ane_academique_id.actived','=',True)])
    apprenant_phone = fields.Char("Téléphone de l'apprenant", related='apprenant_id.apprenant_phone', store=True)
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', 'Année Academique',
                                        help="Selection l'Année Academique")
    class_room_id = fields.Many2one('salle.classe.cafrad',string='Salle de Classe', help="La classe de l'apprenant")
    reponsable_id = fields.Many2one('hr.employee', "Responsable du suivi", required=True,
                                    help="Il s'agit du personel en charge du suivi de l'apprnant")
    fiche_suivi_line_ids = fields.One2many("apprenant.cafrad.suivi.fiche.line",'apprenant_suivi_fiche_id',string="Suivi de l'apprenant")

    date_nais = fields.Date('Date de Naissance')
    lieu_nais = fields.Char("Lieu de Naissance")
    sexe = fields.Selection([('masc', 'Masculin'), ('fem', 'Feminin')], 'Sexe')
    matricule = fields.Char("Matricule de l'apprenant")
    age = fields.Integer(string='Age', default=0, readonly=1)
    date_register = fields.Datetime('Date d\'énregistrement', default=fields.datetime.now())
    school = fields.Selection([('ebase', 'Groupe Scolaire'), ('cef', 'Formation CEF'), ('cafrad', 'Formation BEPENDA')
                                  , ('other', 'Autre Formation'),
                               ('externe', 'Externe')], 'Ecole',
                              required=True, help="L'établissement de l'apprenant")
    email = fields.Char("Email")
    last_diplom = fields.Char("Dernier Diplome")
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Anneée Academique")
    religion_id = fields.Many2one('religion.cafrad', "Religion")
    region_id = fields.Many2one('region.cafrad', string='Région d\'origine', help="La région d'origine de l'apprenant")
    classe_id = fields.Many2one('salle.classe.cafrad', string='Classe', help="La classe de l'apprenant")
    parent_name = fields.Char("Nom et Prenoms des parents")
    parent_phone = fields.Char("Téléphone des parents")
    apprenant_phone = fields.Char("Téléphone de l'apprenant")
    occupation = fields.Text("Dernière Ocuppation ou Ocuppation Actuelle")
    mobility = fields.Boolean("Personne a mobilité reduite ?", defaut=False)
    nature_handicap = fields.Selection([('mal_voyant', 'Mal Voyant(e)'),
                                        ('physiq', ' Handicapé(e) Moteur')],
                                       'Nature de l''Handicap')
    photo = fields.Binary(string="photo de l'apprenant")
    description = fields.Text("Informations complentaires")

    ################################## B/-ACCOMPAGNEMENT PEDAGOGIQUE  ########################################

    speciality_id = fields.Many2one('speciality.cafrad', string='Filière')
    date_start_training = fields.Datetime('Date de debut de la formation', default=fields.datetime.now())
    tutor_name = fields.Char("Noms et Prénoms du Tuteur de la Formation")
    tutor_phone = fields.Char("Téléphone du Tuteur de la Formation")
    quarter_live = fields.Char("Quartier de residence")
    matiere_strong = fields.Char("Matieres Fortes")
    matiere_wek = fields.Char("Solutions Proposées")
    disciplin_observ = fields.Char("Obervations sur la discipline")
    difficulty = fields.Char('Difficicultés Relevées')
    solution = fields.Char("Solution Proposées")
    place_stage = fields.Char("Lieu du Stage Proffesionnel")

    ################################## C/-ACCOMPAGNEMENT A L'INSERTION PROFESSIONELLE ########################################

    nature_parchemin = fields.Char("Nature du Parchemin Obtenu")
    work_type = fields.Char("Choix du type de Travail")
    work_expetation = fields.Char("Poste de travil Sollicité")
    done_activity = fields.Char('Activitées Menées')
    result = fields.Char("Resultat Obtenu")
    first_job_location = fields.Char("Lieu du Premier Emploi")
    first_job_date = fields.Date("Date du Premier Emploi")

    ################################## D/-QUESTIONNAIRE ########################################

    your_ambition = fields.Char("Quelles sont vos ambitions ?")
    your_passion = fields.Char("Quelles sont vos passions ?")
    your_quality = fields.Char("Quelles sont vos Qualités")
    your_defaut = fields.Char('Quels sont vos défauts ?')
    why_formation = fields.Text("Pourquoi avoir choisi cette formation ?")
    souhait_end = fields.Char("Quel est votre souhait après la formation ?")
    type_emploi_end = fields.Char("Aimeriez-vous travailler en emploi salarié ou en Auto emploi ? ?")
    why = fields.Char("Pourquoi ?")
    end_word = fields.Char("Votre mot de fin")

    ################################## E/-FICHE DE PLACEMENT EN STAGE PROFESSIONNEL ########################################

    date_start_stage = fields.Date("Date de debut de stage")
    date_end_stage = fields.Date("Date de fin de stage")
    theme_stage = fields.Char("Theme de Soutenance")
    encadreur_aca = fields.Many2one("teacher.cafrad", "Encadreur Academique")
    encadreur_pro = fields.Many2one("res.partner", "Encadreur Professionel")
    partener_insert = fields.Many2one("res.partner", "Entreprise d'insertion")
    account_insert = fields.Char("Activitée et lieu d'auto inserton")

    state_suivi = fields.Selection([('draft', 'En Attente d''insertion'),
                                    ('running', 'En Cours d''insertion'),
                                    ('insertalone', 'Inseré(e) a son compte'),
                                    ('insert', 'Inseré(e) dans une entreprise')],
                                   string='Situation', default='draft')

    @api.onchange('apprenant_id')
    def _onchange_apprenant_id(self):
        for rec in self:
            if rec.apprenant_id:
                rec.ane_academique_id = rec.apprenant_id.ane_academique_id and rec.apprenant_id.ane_academique_id.id
                rec.date_nais= rec.apprenant_id.date_nais
                rec.sexe = rec.apprenant_id.sexe
                rec.matricule = rec.apprenant_id.matricule
                rec.religion_id = rec.apprenant_id.religion_id and rec.apprenant_id.religion_id.id
                rec.region_id = rec.apprenant_id.region_id and rec.apprenant_id.region_id.id
                rec.class_room_id = rec.apprenant_id.classe_id and rec.apprenant_id.classe_id.id
                rec.occupation = rec.apprenant_id.occupation
                rec.mobility = rec.apprenant_id.mobility
                rec.nature_handicap = rec.apprenant_id.nature_handicap
                rec.speciality_id = rec.apprenant_id.speciality_id and rec.apprenant_id.speciality_id.id
                rec.school = rec.apprenant_id.school
                rec.lieu_nais = rec.lieu_nais
                rec.apprenant_phone = rec.apprenant_id.apprenant_phone

    @api.model
    def create(self, vals):
        # vals['ane_academique_id'] = "Your Value"
        apprenant_id = vals.get('apprenant_id')
        apprenant = self.env['apprenant.cafrad'].browse(apprenant_id)
        vals.update({
            'ane_academique_id': apprenant.ane_academique_id and apprenant.ane_academique_id.id,
            'class_room_id': apprenant.classe_id and apprenant.classe_id.id,
            'apprenant_phone': apprenant.apprenant_phone,
            'matricule':apprenant.matricule
        })
        res = super(apprenant_cafrad_suivi_fiche, self).create(vals)
        return res

    def write(self, vals):
        apprenant_id = vals.get('apprenant_id')
        apprenant = self.env['apprenant.cafrad'].browse(apprenant_id)
        vals.update({
            'ane_academique_id': apprenant.ane_academique_id and apprenant.ane_academique_id.id,
            'class_room_id': apprenant.classe_id and apprenant.classe_id.id,
            'apprenant_phone': apprenant.apprenant_phone,
            'matricule': apprenant.matricule,
        })
        res = super(apprenant_cafrad_suivi_fiche, self).write(vals)
        return res


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
            if not record.partener_insert:
                raise UserError(_("Alerte !!! Veillez entrer le nom de l'entreprise d'insertion"))

        return self.write({"state_suivi": 'insert'})

    def set_to_insertalone(self):
        for record in self:
            if record.state_suivi not in ['running']:
                raise UserError(_("Alerte !!! pour faire passer le suivi cet "
                                  "apprenant a insertion a son compte, "
                                  "rassurer vous qu'il soit d'abord en cours d'insertion"))
            if not record.account_insert:
                raise UserError(_("Alerte !!! Veillez entrer l'activité et le lieu d'insertion"))

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






