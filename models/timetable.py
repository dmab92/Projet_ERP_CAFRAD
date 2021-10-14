# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class time_table_cafrad(models.Model):
    """Defining model for time table."""
    _description = 'Emploi de temps au CAFRAD'
    _name = 'time.table.cafrad'


    @api.model
    def _get_default_academic_year(self):
        academic_year_obj = self.env['ane.academiq.cafrad']
        academic_year_id = academic_year_obj.search([('actived', '=', True)], limit=1)
        return academic_year_id and academic_year_id.id or False

    name = fields.Char('Description')
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', 'Année Academique',
                                        default=lambda self: self._get_default_academic_year(),required=True,
                                  help="Selection l'Année Academique")
    school = fields.Selection([('ebase', 'Groupe Scolaire'), ('cef', 'Formation CEF'), ('cafrad', 'Formation BEPENDA')
                                  , ('other', 'Autre Formation'),
                                   ('externe', 'Externe')], 'Ecole',
                              required=True, help="L'établissement de l'apprenant")

    timetable_ids = fields.One2many('time.table.line.cafrad', 'table_id', 'Emploi de temps')
    start_date = fields.Date('Date de Debut')
    end_date = fields.Date('Date de fin')
    class_room_id = fields.Many2one('salle.classe.cafrad', 'Salle de Classe',required=True)
    state = fields.Selection([('draft', 'Brouillon'),
                              ('validated', 'Validé')], default='draft',string="Etat")
    matiere_id = fields.Many2one("speciality.cafrad", String="Filiere")

    def button_validate(self):
        return self.write({'state': 'validated'})

    def print_time_table(self):
        # datas = {
        #
        # }
        return self.env.ref('cafrad_app.action_report_time_table').report_action(self)


class time_table_line_cafrad(models.Model):
    """Defining model for time table."""

    _description = 'Lignes d''emploi de temps au CAFRAD'
    _name = 'time.table.line.cafrad'
    _rec_name = 'table_id'

    teacher_id = fields.Many2one('teacher.cafrad', 'Enseignant',
                                 help="Selectionnez l'enseignant")
    matiere_id = fields.Many2one('matiere.cafrad', 'Matiere',
                                 help="Selectionnez la matiere")

    table_id = fields.Many2one('time.table.cafrad', 'Emploi de temps')

    start_time = fields.Float('Heure de Debut', required=True)
    end_time = fields.Float('Heure de Fin', required=True)

    week_day = fields.Selection([('monday', 'Lundi'),
                                 ('tuesday', 'Mardi'),
                                 ('wednesday', 'Mercredi'),
                                 ('thursday', 'Jeudi'),
                                 ('friday', 'Vendredi'),
                                 ('saturday', 'Samedi'),
                                 ], "Jour de la Semaine")

    class_room_id = fields.Many2one('salle.classe.cafrad', 'Salle de Classe')
