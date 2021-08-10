# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


class time_table_cafrad(models.Model):
    """Defining model for time table."""
    _description = 'Emploi de temps au CAFRAD'
    _name = 'time.table.cafrad'

    name = fields.Char('Description')
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', 'Année Academique',
                                  required=True,
                                  help="Selection l'Année Academique")
    school = fields.Selection([('ebase', 'Education de base'), ('cef', 'CEF')], 'Ecole',
                              help="L'etablissement au quel appartient la salle")

    timetable_ids = fields.One2many('time.table.line.cafrad', 'table_id', 'Emploi de temps')

    class_room_id = fields.Many2one('salle.classe.cafrad', 'Salle de Classe')
    state = fields.Selection([('draft', 'Brouillon'),
                              ('validated', 'Validé')], "Etat")


class time_table_line(models.Model):
    """Defining model for time table."""

    _description = 'Lignes d''emploi de temps au CAFRAD'
    _name = 'time.table.line.cafrad'
    _rec_name = 'table_id'

    teacher_id = fields.Many2one('teacher.cafrad', 'Enseignant',
                                 help="Selectionnez l'enseignant")
    matiere_id = fields.Many2one('matiere.cafrad', 'Matiere',
                                 help="Selectionnez la matiere")

    table_id = fields.Many2one('time.table.cafrad', 'Emploi de temps')

    start_time = fields.Char('Heure de Debut', required=True)
    end_time = fields.Char('Heure de Fin', required=True)

    week_day = fields.Selection([('monday', 'Lundi'),
                                 ('tuesday', 'Mardi'),
                                 ('wednesday', 'Mercredi'),
                                 ('thursday', 'Jeudi'),
                                 ('friday', 'Vendredi'),
                                 ('saturday', 'Samedi'),
                                 ('sunday', 'Dimanche')], "Jour de la Semaine")

    class_room_id = fields.Many2one('salle.classe.cafrad', 'Salle de Classe')
