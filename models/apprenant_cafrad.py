# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, Warning, ValidationError
from odoo.tools.translate import _

class apprenant_cafrad(models.Model):
    _name = "apprenant.cafrad"
    _description = "Apprenant du CAFRAD"
    _rec_name = 'name'
    _order = 'id DESC'

    def _get_next_reference(self):
        query = """SELECT COUNT(id) AS ligne FROM apprenant_cafrad"""
        self.env.cr.execute(query)
        data = self.env.cr.fetchone()[0]
        year = time.strftime('%Y')
        sort_year = ''

        # on recupère les 2 derniers chiffres
        y = 0
        for i in year:
            y += 1
            if y < 3:
                continue
            sort_year = sort_year + str(i)

        if not data or data == 0:
            return 'MAT/00001/' + sort_year

        if data < 10:
            return 'MAT/0000' + str(data + 1) + '/' + sort_year

        if data < 100 and data >= 10:
            return 'MAT/000' + str(data + 1) + '/' + sort_year

        if data < 1000 and data >= 100:
            return 'MAT/00' + str(data + 1) + '/' + sort_year

        if data < 10000 and data >= 1000:
            return 'MAT/0' + str(data + 1) + '/' + sort_year

        if data < 100000 and data >= 10000:
            return 'MAT' + str(data + 1) + '/' + sort_year

    @api.model
    def _get_default_academic_year(self):
        academic_year_obj = self.env['ane.academiq.cafrad']
        academic_year_id = academic_year_obj.search([('actived', '=', True)], limit=1)
        return academic_year_id and academic_year_id.id or False



    #FIELDS
    name = fields.Char("Nom de l'apprenant", required=True)
    date_nais = fields.Date('Date de Naissance',default=datetime.today().date())
    lieu_nais = fields.Char("Lieu de Naissance")
    sexe = fields.Selection([('masc', 'Masculin'), ('fem', 'Feminin')], 'Sexe',required=True)
    matricule = fields.Char("Matricule de l'apprenant", readonly="True", default=lambda self: self._get_next_reference())
    age = fields.Integer('Age',  compute="compute_age")
    date_register = fields.Datetime('Date d\'énregistrement', default=fields.datetime.now())
    school = fields.Selection([('ebase', 'Groupe Scolaire'),
                               ('cef', 'Formation CEF'),
                               ('cafrad', 'Formation BEPANDA'),
                               ('other', 'Autre Formation'),
                               ('externe', 'Externe')], 'Ecole',
                              required=True,help="L'établissement de l'apprenant")

    ancien_new = fields.Selection([('ancien', 'Ancien'),
                                   ('new', 'Nouveau')] ,'Ancien/Nouveau', default='new')
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Annee Academique",
                                        default=lambda self: self._get_default_academic_year())
    religion_id= fields.Many2one('religion.cafrad',"Religion")
    region_id = fields.Many2one('region.cafrad',
                                string='Région d\'origine', help="La région d'origine de l'apprenant")
    classe_id = fields.Many2one('salle.classe.cafrad', required=True,
                                string='Classe', help="La classe de l'apprenant")
    parent_name = fields.Char("Nom et Prenoms des parents")
    parent_phone = fields.Char("Téléphone des parents")
    apprenant_phone = fields.Char("Téléphone de l'apprenant")
    occupation = fields.Text("Dernière Ocuppation ou Ocuppation Actuelle")
    mobility = fields.Boolean("Personne a mobilité reduite ?", defaut=False)
    nature_handicap = fields.Selection([('mal_voyant', 'Mal Voyant(e)'), ('physiq', ' Handicapé(e) Moteur')], 'Nature de l''Handicap')
    photo = fields.Binary(string="photo de l'apprenant")
    urgence_phone = fields.Char("Téléphone d'urgence")
    urgence_person = fields.Char("Nom et Prénoms")
    state = fields.Selection([('prospet','Prospet'),('student','Apprenant')], default='prospet')
    hotel_client = fields.Boolean("Est client pour l'Hebergement ?", defaut=False)
    description = fields.Text("Informations complentaires")
    attachment_ids = fields.Many2many("ir.attachment")
    annuel_average = fields.Float("Moyenne Annuelle")
    student_upgra_id = fields.Many2one('apprenant.cafrad.upgrade',string='Admission')

    speciality_id = fields.Many2one('speciality.cafrad', string='Filière')
    state_admission = fields.Selection([('draft', 'En attente de decision'),
                                        ('redouble', 'Redouble'),
                                        ('admis', 'Admis')],  string='Situation',default='draft')

    payment_ids = fields.One2many('payment.apprenant', 'apprenant_id', string='Mes Payements')

    #-------------------------------------SURCHARGE DE L'ORM----------------------------#

    @api.depends('date_nais')
    def compute_age(self):
        for record in self:
            record.age=0
            if record.date_nais:
                d1 = record.date_nais
                d2 = datetime.today().date()
                record.age = relativedelta(d2, d1).years
        else:
            pass

    def button_admission(self):
        apprenant_obj = self.env['apprenant.cafrad']
        for record in self:
            if record.annuel_average < record.classe_id.min_average :
                raise UserError(_("Alerte! la moyenne de cet(te) appprenant(e)  est inférieure a la note minimale "
                                  "requise  pour l'admision en classe superieure"))
            #print("Hello World,Hello World,Hello WorldHello World")
            vals ={
                'name': record.name,
                'date_nais': record.date_nais,
                'lieu_nais': record.lieu_nais,
                'sexe':record.sexe,
                'matricule':record.matricule,
                'apprenant_phone': record.apprenant_phone,
                'date_register': record.date_register,
                'school':record.school,
                'ancien_new': 'ancien',
                'ane_academique_id': record.ane_academique_id.next_academique_id and record.ane_academique_id.next_academique_id.id,
                'religion_id': record.religion_id,
                'region_id':record.region_id,
                'classe_id':record.classe_id.next_class and record.classe_id.next_class.id,
                'parent_name':record.parent_name,
                'parent_phone':record.parent_phone,
                'occupation':'',
                'mobility':record.mobility,
                'nature_handicap':record.nature_handicap,
                'photo': record.photo,
                'urgence_phone':record.urgence_phone,
                'urgence_person': record.urgence_person,
                'state': 'student',
                'hotel_client': 'False',
                'description': record.description,
                'annuel_average':'',
                #'next_class': '',
                'state_admission':'draft',
            }
            apprenant_obj.create(vals)
        return self.write({"state_admission": 'admis'})

    def button_redouble(self):
        for record in self:
            if record.annuel_average > record.classe_id.min_average :
                raise UserError(_("Alerte! la moyenne de cet élève est "
                                  "superieure a la note minimale requise  pour l'admision en classe superieure"))
        return self.write({"state_admission": 'redouble'})

    def button_validate(self):
        partener_obj = self.env['res.partner']
        for record in self:
            vals ={
                'name': record.name,
                'phone': record.apprenant_phone,
                'street': record.matricule,
                'company_type': 'person',

            }
            partener_obj.create(vals)
        return super(apprenant_cafrad, self).write({"state": 'student'})


    def button_generer(self):
        #payment_obj = self.env['payment.apprenant']
        sales_ids = self.env['sale.order'].search([('origin', '=', self.matricule),
                                                   ('state', 'in', ['sale','done'])])
        for record in self:
            if len(sales_ids) == 0:
                raise UserError(_("Desole !!!! Cet apprenant n'a  encore effectue aucun payment pour cette année academique"))
            else :
                for sale in sales_ids:
                        vals = {
                             'name': sale.name,
                             'matricule': sale.origin,
                             'ane_academique_id': sale.ane_academique_id and sale.ane_academique_id.id,
                             'date_payement': sale.date_order,
                             'montant': sale.amount_total,
                             'state': sale.state,
                             'apprenant_id': self.id
                          }
                        record.write({'payment_ids': [[0, 0, vals]]})



class payment_apprenant(models.Model):
    _name = "payment.apprenant"
    _description = "Payements des apprenants du CAFRAD"
    _rec_name = 'name'
    _order = 'id DESC'

    name  = fields.Char("Numero de payment")
    matricule= fields.Char("Matricule")
    apprenant_id = fields.Many2one('apprenant.cafrad',string="Apprenant")
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Annee Academique")
    date_payement = fields.Datetime('Date du payment')
    montant  = fields.Integer("Montant")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('sent', 'Validé'),
        ('sale', 'Validé'),
        ('done', 'Validé'),
        ('cancel', 'Annulé'),
    ], string='Etat', readonly=True)


    #lines = fields.One2many("sale.order.line", string="Line de payements")


# class payment_apprenant_line(models.Model):
#     _name = "payment.apprenant.line"
#     _description = "Payements des apprenants du CAFRAD"
#     _rec_name = 'name'
#     _order = 'id DESC'
#
#     name = fields.Char("Numero de payment")
#     price_unit = fields.Char("Prix Unitaire")
#     apprenant_id = fields.Many2one('apprenant.cafrad', string="Apprenant")
#     ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Annee Academique")
#     date_payement = fields.Datetime('Date du payment')
#     montant = fields.Char("Montant")
