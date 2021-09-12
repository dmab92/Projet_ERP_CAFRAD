# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class employee_presence_cafrad(models.Model):
    _name = "employee.presence.cafrad"
    _description = "Gestion des presences des employees au CAFRAD"
    _rec_name = 'name'
    _order = 'id DESC'

    @api.model
    def _get_default_academic_year(self):
        academic_year_obj = self.env['ane.academiq.cafrad']
        academic_year_id = academic_year_obj.search([('active', '=', True)], limit=1)
        return academic_year_id and academic_year_id.id or False

    # @api.model
    # def _get_default_compagny(self):
    #     compagny_obj = self.env['res.company']
    #     compagny_id = compagny_obj.search([('user_id', '=', self.env.uid)], limit=1)
    #     return compagny_id and compagny_id.id or False

    name = fields.Char("Description", required=1)
    ane_academique_id = fields.Many2one('ane.academiq.cafrad', "Année Académique",
                                        default=lambda self: self._get_default_academic_year(), required=True)
    company_id = fields.Many2one("res.company", 'Etablissement', required='1', default=lambda self: self.env.user.company_id)
    date_register = fields.Datetime('Date du jour', default=fields.datetime.now())
    employee_ids = fields.One2many('hr.employee', 'presence_id', copy=True, string="Les Personnels ")
    state = fields.Selection([('draft', 'Brouillon'),
                              ('validated', 'Validé')], default='draft', string="Etat")

    #-------------------SURCHARGE DE L'ORM--------------------#

    @api.onchange('company_id')
    def _onchange_company_id(self):
        employee_by_ids = self.env['hr.employee'].search([('company_id', '=', self.company_id.id)])
        for rec in self:
            if rec.company_id:
                lines = [(5, 0, 0)]
                for line in employee_by_ids:
                    vals = {
                         'name': line.name,
                         'company_id': line.company_id,
                         'job_id':line.job_id.id,
                         'mobile_phone': line.mobile_phone,
                            }
                    lines.append((0, 0, vals))
                rec.employee_ids = lines

    def button_validate(self):
        return self.write({'state': 'validated'})