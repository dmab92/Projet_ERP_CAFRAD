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

    name = fields.Char("Nom de la classe", required=True)
    reponsable_id = fields.Many2one('hr.employee', "Responsable", help="Il s'agit de l'enseigant en charge de la salle, "
          "il peut etre une maitresse ou un prof titulaire")
    bool_cm2  = fields.Boolean('Est un CM2 ?')



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