# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class apprenant_cafrad_upgrade(models.Model):
    _name = "apprenant.cafrad.upgrade"
    _description = "Passage en classe superieure au CAFRAD"
    _rec_name = 'name'
    _order = 'id DESC'

    @api.model
    def _get_default_academic_year(self):
        academic_year_obj = self.env['ane.academiq.cafrad']
        academic_year_id = academic_year_obj.search([('active', '=', True)], limit=1)
        return academic_year_id and academic_year_id.id or False

    name = fields.Char("Description", required=1)
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Année Académique",
                                        default=lambda self: self._get_default_academic_year(), required=True)
    class_room_id = fields.Many2one('salle.classe.cafrad', 'Salle de Classe',required=True, )
    date_register = fields.Datetime('Date d\'énregistrement', default=fields.datetime.now())
    apprenant_ids = fields.One2many('apprenant.cafrad', 'student_upgra_id', copy=True, string="Les Apprenants")


    @api.onchange('class_room_id','ane_academique_id')
    def _onchange_class_room_id(self):
        evaluation_line_ids = self.env['apprenant.cafrad'].search([('classe_id', '=', self.class_room_id.id),
                                                             ('ane_academique_id', '=', self.ane_academique_id.id)])
        for rec in self:
            if rec.class_room_id:
                lines = [(5, 0, 0)]
                for line in evaluation_line_ids:
                    vals = {
                         'name': line.name,
                         'annuel_average': line.annuel_average,
                         'classe_id':line.classe_id.id
                            }
                    lines.append((0, 0, vals))
                rec.apprenant_ids = lines


