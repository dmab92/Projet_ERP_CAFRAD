# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class religion_cafrad(models.Model):
    _name = "religion.cafrad"
    _description = " Religion des apprenants du CAFRAD"
    _order = 'id DESC'

    name = fields.Char("Nom de la réligion")


class region_cafrad(models.Model):
    _name = "region.cafrad"
    _description = " Region des apprenants du CAFRAD"
    _order = 'id DESC'

    name = fields.Char("Nom de la région", required=True)


class salle_classe_cafrad(models.Model):
    _name = "salle.classe.cafrad"
    _description = "Classe des apprenants du CAFRAD"
    _order = 'id DESC'

    FIXED_CLASS_TYPE = [
        ('0', 'CAFRAD'),
        ('1', 'Maternelle 1'),
        ('2', 'Maternelle 2'),
        ('3', 'Maternelle 3'),
        ('4', 'SIL'),
        ('5', 'CP'),
        ('6', 'CE1'),
        ('7', 'CE2'),
        ('9', 'CM1'),
        ('10', 'CM2'),
        ('11', 'HOTELLERIE 1'),
        ('12', 'HOTELLERIE 2'),
        ('13', 'HOTELLERIE 3'),
        ('14', 'COUTURE 1'),
        ('15', 'COUTURE 2'),
        ('16', 'COUTURE 3'),
        ('18', 'PATISSERIE 1'),
        ('19', 'PATISSERIE 2'),
        ('20', 'PATISSERIE 3')
    ]


    @api.model
    def _get_default_academic_year(self):
        academic_year_obj = self.env['ane.academiq.cafrad']
        academic_year_id = academic_year_obj.search([('active', '=', True)], limit=1)
        return academic_year_id and academic_year_id.id or False

    name = fields.Char("Nom de la classe", required=True)
    reponsable_id = fields.Many2one('hr.employee', "Responsable", help="Il s'agit de l'enseigant en charge de la salle, "
          "il peut etre une maitresse ou un prof titulaire")
    bool_cm2  = fields.Boolean('Est un CM2 ?')

    ane_academique_id = fields.Many2one('ane.academiq.cafrad', 'Année Academique',
                                        default=lambda self: self._get_default_academic_year(),
                                        required=True,
                                        help="Selection l'Année Academique")

    code = fields.Selection(FIXED_CLASS_TYPE, 'Code')

class speciality_cafrad(models.Model):
    _name = "speciality.cafrad"
    _description = "Filere de formation des apprenants du CAFRAD"
    _order = 'id DESC'

    name = fields.Char("Nom de la filiere", required=True)
    responsable_id = fields.Many2one('hr.employee',
                                  "Responsable",
                                  help="Il s'agit du responsable de la filiere")


class matiere_cafrad(models.Model):
    _name = "matiere.cafrad"
    _description = "Matiere de formation des apprenants du CAFRAD"
    _order = 'id DESC'

    name = fields.Char("Nom de la filiere", required=True)
    responsable_id = fields.Many2one('teacher.cafrad',
                                  "Responsable",
                                  help="Il s'agit du responsable de la matiere")