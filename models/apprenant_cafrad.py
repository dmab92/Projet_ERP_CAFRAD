# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
import time
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
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

    #FIELDS
    name = fields.Char("Nom de l'apprenant")
    date_nais = fields.Date('Date de naissance')
    lieu_nais = fields.Char("Lieu de Naissance")
    sexe = fields.Selection([('masc', 'Masculin'), ('fem', 'Feminin')], 'Sexe')
    matricule = fields.Char("Matricule de l'apprenant", readonly="True", default=lambda self: self._get_next_reference())
    age = fields.Integer('Age', compute="compute_age")
    date_register = fields.Datetime('Date d\'énregistrement', default=fields.datetime.now())
    school = fields.Selection([('ebase', 'Education de base'), ('cef', 'CEF')],'Ecole'
                                     help="L'etablissement de l'apprenant")
    ancien_new = fields.Selection([('ancien', 'Ancien'), ('new', 'Nouveau')], 'Ancien/Nouveau', required=True)
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Annee Academique", required=True)
    religion_id= fields.Many2one('religion.cafrad',"Religion")
    region_id = fields.Many2one('region.cafrad',
                                string='Région d\'origine', help="La région d'origine de l'apprenant")
    classe_id = fields.Many2one('salle.classe.cafrad',
                                string='Classe', help="La classe de l'apprenant")

    parent_name= fields.Char("Nom et Prenoms des parents")
    parent_phone = fields.Char("Telephone des parents")
    apprenant_phone= fields.Char("Telephone de l'apprenant")
    occupation = fields.Char("Derniere Ocuppation ou Ocuppation Actuelle")
    mobility=  fields.Boolean("Personne a mobilite reduite ?", defaut=False)
    photo = fields.Binary(string="photo de l'apprenant")


    #FUNCTIONS

    @api.depends("date_nais")
    def compute_age(self):
        for record in self:
            if record.date_nais:
                d1 = datetime.datetime.strptime(record.date_nais, "%Y-%m-%d").date()
                rd = relativedelta(date.today(), d1)
                record.age = rd.years

#
# class religion_cafrad(models.Model):
#     _name = "religion.cafrad"
#     _description = " Religion des apprenants du CAFRAD"
#     _order = 'id DESC'
#
#     name = fields.Char("Nom de la réligion")
#
#
#
# class region_cafrad(models.Model):
#     _name = "region.cafrad"
#     _description = " Region des apprenants du CAFRAD"
#     _order = 'id DESC'
#
#     name = fields.Char("Nom de la région")
#
#
# class classe_cafrad(models.Model):
#     _name = "classe.cafrad"
#     _description = "Classe des apprenants du CAFRAD"
#     _order = 'id DESC'
#
#     name = fields.Char("Nom de la classe")
#
#
#
# class speciality_cafrad(models.Model):
#     _name = "speciality.cafrad"
#     _description = "Filere de formation des apprenants du CAFRAD"
#     _order = 'id DESC'
#
#     name = fields.Char("Nom de la filiere")
#     responsable = fields.Many2one('')