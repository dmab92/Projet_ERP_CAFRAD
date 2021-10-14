# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, Warning, ValidationError


class apprenant_cafrad_upgrade(models.Model):
    _name = "apprenant.cafrad.upgrade"
    _description = "Passage en classe superieure au CAFRAD"
    _rec_name = 'name'
    _order = 'id DESC'

    @api.model
    def _get_default_academic_year(self):
        academic_year_obj = self.env['ane.academiq.cafrad']
        academic_year_id = academic_year_obj.search([('actived', '=', True)], limit=1)
        return academic_year_id and academic_year_id.id or False

    name = fields.Char("Description", required=1)
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Année Académique",
                                        default=lambda self: self._get_default_academic_year())
    class_room_id = fields.Many2one('salle.classe.cafrad', 'Salle de Classe',required=True)
    date_register = fields.Datetime('Date d\'énregistrement', default=fields.datetime.now())
    apprenant_ids = fields.One2many('apprenant.cafrad', 'student_upgra_id', copy=True, string="Les Apprenants")
    apprenant_count = fields.Integer(
        string="Nombre d'apprenants", compute='_get_apprenant_count', store=True)


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

    @api.constrains('apprenant_ids')
    def _check_values(self):
        for record in self:
            for line in record.apprenant_ids :
                if line.annuel_average < 0.0 or line.annuel_average > 20.0:
                    raise UserError(_("'Alert !!!! La moyenne minimale doit etre comprise entre 0 et 20.'"))

    def set_validated(self):
        for record in self:
            if record.apprenant_ids:
                for line in record.apprenant_ids:
                    line.button_admission()
            else:
                raise UserError(_("'Alert !!! Veillez choisir une classe svp'"))

    @api.depends('apprenant_ids')
    def _get_apprenant_count(self):
        for r in self:
            r.apprenant_count = len(r.apprenant_ids)




