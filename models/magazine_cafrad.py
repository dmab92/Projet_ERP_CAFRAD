# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class magazine_cafrad(models.Model):
    _description = 'Magazine du  CAFRAD'
    _name = 'magazine.cafrad'
    _rec_name = 'name'
    _order = 'id DESC'

    name = fields.Char('Nom', required=True)
    article_ids = fields.One2many('article.magazine.cafrad', 'mazine_id', 'Articles du Magazine')
    employee_id = fields.Many2one('hr.employee', string="Redacteur en chef")
    publication_date = fields.Date('Date de publication')
    attachment_ids = fields.Many2many("ir.attachment", string="Inserer le Magazine ici")

class magazine_line_cafrad(models.Model):
    """Defining model for time table."""

    _description = 'Lignes de magazine au CAFRAD'
    _name = 'article.magazine.cafrad'
    _rec_name = 'description'

    partner_id = fields.Many2one('res.partner', string="Intervenant")
    description = fields.Text("Description ou Resumé de l'article")
    role = fields.Selection([('redateurChef', 'Recdateur en Chef'),
                             ('redacteur', 'Redacteur'),
                             ('lecteur', 'Lecteur'),
                             ('infographe', 'Infographe'),
                             ('directeur', 'Directeur de publication')
                                 ],"Role")
    attachment_ids = fields.Many2many("ir.attachment", string="Inserer l'article ici")
    mazine_id = fields.Many2one('magazine.cafrad', 'Magazine')

class redacteur_magazine_cafrad(models.Model):
    _description = 'Redacteurs de Magazine au  CAFRAD'
    _name = 'redac.magazine.cafrad'
    _rec_name = 'employee_id'
    _order = 'id DESC'

    employee_id = fields.Many2one('hr.employee', string="Nom du Redacteur")
    phone = fields.Char("Phone", related='employee_id.phone')
    