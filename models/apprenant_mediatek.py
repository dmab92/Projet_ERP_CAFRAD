# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
import time
from odoo.tools.translate import _
from odoo.exceptions import UserError


class mediatek_cafrad(models.Model):
    _name = "mediatek.cafrad"
    _description = "Mediatheque  du CAFRAD"
    _order = 'id DESC'

    def _get_next_reference(self):
        query = """SELECT COUNT(id) AS ligne FROM mediatek_cafrad"""
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
            return 'LOC/001/' + sort_year

        if data < 10:
            return 'LOC/00' + str(data + 1) + '/' + sort_year

        if data < 100 and data >= 10:
            return 'LOC/0' + str(data + 1) + '/' + sort_year

        if data < 1000 and data >= 100:
            return 'LOC/' + str(data + 1) + '/' + sort_year

    identifiant = fields.Char("Identifiant", readonly="True", default=lambda self: self._get_next_reference())
    profession = fields.Char("Profession")
    phone_number = fields.Char("Telephone")
    motif = fields.Char("Motif")
    partner_id = fields.Many2one('res.partner', "Abonné(e)", required=True)
    sexe = fields.Selection([('masc', 'Masculin'), ('fem', 'Feminin')], 'Sexe')
    livre_id = fields.Many2one('livre.cafrad', 'Livre')
    categori_id = fields.Many2one('cafrad.book.categorie', 'Categorie', related='livre_id.categori_id')
    date_register = fields.Date("Date d\'enregistrement")

    date_out = fields.Datetime('Date de Sortie', default=fields.datetime.now())
    date_in = fields.Datetime('Date de retour Programmer', required=True)
    state = fields.Selection([('draft', 'Brouillon'),
                              ('loan', 'Emprunter'),
                              ('back', 'Retouner')], default='draft', string="Etat")

    def name_get(self):
        '''Method to display name and code'''
        return [(rec.id, ' ' + str(rec.identifiant) + '/' + str(rec.partner_id.name)) for rec in self]


    def button_loan(self):
        loan_ids = self.env['mediatek.cafrad'].search([('partner_id', '=', self.partner_id.id),('state', '=', 'loan')])
        if len(loan_ids)>0:
            raise UserError(_(" Desolez cet(te) abonné(e) ne  plus emprunter un livre car il/elle n'a pas encore "
                              "retourné(e) un precedent livre"))
        return self.write({'state': 'loan'})

    def button_back(self):
        return self.write({'state': 'back'})

class livre_cafrad(models.Model):
    _name = "livre.cafrad"
    _description = "Livres du CAFRAD"
    _order = 'id DESC'
    _rec_name ='titre'

    def _get_next_reference(self):
        query = """SELECT COUNT(id) AS ligne FROM livre_cafrad"""
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
            return 'BOOK/001/' + sort_year

        if data < 10:
            return 'BOOK/00' + str(data + 1) + '/' + sort_year

        if data < 100 and data >= 10:
            return 'BOOK/0' + str(data + 1) + '/' + sort_year

        if data < 1000 and data >= 100:
            return 'BOOK/' + str(data + 1) + '/' + sort_year

    identifiant = fields.Char("Identifiant", readonly="True", default=lambda self: self._get_next_reference())
    titre = fields.Char("Titre",  required=True)
    date_register = fields.Date("Date d\'enregistrement",default=fields.datetime.now())
    date_out = fields.Date('Date de sortie')
    autor = fields.Char("Auteur", required=True)
    categori_id = fields.Many2one('cafrad.book.categorie', 'Categorie')

class book_categori_cafrad(models.Model):
    _name = "cafrad.book.categorie"
    _description = "Categorie de livres  du CAFRAD"
    _order = 'id DESC'

    name = fields.Char("Nom de la Categorie", required=True)
    livres_ids= fields.One2many('livre.cafrad','categori_id', string="Livres")















    #FUNCTIONS

    # @api.depends("date_nais")
    # def compute_age(self):
    #     for record in self:
    #         if record.date_nais:
    #             d1 = datetime.datetime.strptime(record.date_nais, "%Y-%m-%d").date()
    #             rd = relativedelta(date.today(), d1)
    #             record.age = rd.years



