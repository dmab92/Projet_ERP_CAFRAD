# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
import time
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo.tools.translate import _


class teacher_cafrad(models.Model):
    _name = "teacher.cafrad"
    _description = "Enseignant du CAFRAD"
    _rec_name = 'employee_id'
    _order = 'id DESC'

    def _get_next_reference(self):
        query = """SELECT COUNT(id) AS ligne FROM teacher_cafrad"""
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
            return 'EN/001/' + sort_year

        if data < 10:
            return 'EN/00' + str(data + 1) + '/' + sort_year

        if data < 100 and data >= 10:
            return 'EN/0' + str(data + 1) + '/' + sort_year

        if data < 1000 and data >= 100:
            return 'EN/' + str(data + 1) + '/' + sort_year



    #FIELDS
    #name = fields.Char("Nom de l'enseignant")
    employee_id = fields.Many2one('hr.employee',string="Nom de l'enseignant")
    sexe = fields.Selection([('masc', 'Masculin'), ('fem', 'Feminin')], 'Sexe')
    matricule = fields.Char("Matricule de l'enseignant", readonly="True", default=lambda self: self._get_next_reference())
    #age = fields.Integer('Age', compute="compute_age")
    date_register = fields.Datetime('Date d\'énregistrement', default=fields.datetime.now())
    school = fields.Selection([('ebase', 'Education de base'), ('cef', 'CEF')],'Ecole',
                                     help="L'etablissement de l'apprenant")
    teacher_phone= fields.Char("Telephone de l'enseignant")
    photo = fields.Binary(string="photo de l'Enseigant")
    attachment_ids = fields.Many2many("ir.attachment")


    #FUNCTIONS

    # @api.depends("date_nais")
    # def compute_age(self):
    #     for record in self:
    #         if record.date_nais:
    #             d1 = datetime.datetime.strptime(record.date_nais, "%Y-%m-%d").date()
    #             rd = relativedelta(date.today(), d1)
    #             record.age = rd.years



