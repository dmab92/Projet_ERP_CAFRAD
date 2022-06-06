# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class visiteur_cafrad(models.Model):
    """Defining model for radio camando."""
    _description ="Visiteurs du CAFRAD"
    _name = 'visiteur.cafrad'

    name  = fields.Char("Noms et Prénoms")
    user_id = fields.Many2one('res.users', 'Recu par',default=lambda self: self.env.user)

    date_register = fields.Datetime('Date et Heure de la visite')
    phone = fields.Char("Telephone" )
    motif = fields.Text("Motif de la visite")
    email=  fields.Char("Email")
    remarques= fields.Text("Informations Particulieres")

