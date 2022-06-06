# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class radio_cafrad(models.Model):
    """Defining model for radio camando."""
    _description = 'Radio casmando au CAFRAD'
    _name = 'radio.cafrad'
    _rec_name ='emission_id'

    emission_id = fields.Many2one('emission.radio.cafrad',"Emision", required=1)

    presentateur_id = fields.Many2one('hr.employee', "Presentation")

    programe_owner_id = fields.Many2one('hr.employee', "Le charge des programmes")

    date_hour = fields.Datetime('Date et Heure')

    colaboration_ids = fields.Many2many('hr.employee', string="Collaborations")

    invites_ids = fields.Many2many("res.partner", string="Invites du programmes")

    radioline_ids = fields.One2many('line.radio.cafrad', 'radio_id',"Details")


    def print_conducteur_antene(self):
        # datas = {
        #
        # }
        return self.env.ref('cafrad_app.action_report_conducteur_antene').report_action(self)

class emision_radio_cafrad(models.Model):
    """Defining model for emsion radio camando."""
    _description = 'Emission Radio casmando au CAFRAD'
    _name = 'emission.radio.cafrad'

    name = fields.Char("Nom de l'emission", required=1)
    presentateur_id = fields.Many2one('hr.employee', "Presentation")



class radio_line_cafrad(models.Model):
    """Defining model for time table."""

    _description = 'Lignes de radio au CAFRAD'
    _name = 'line.radio.cafrad'
    #_rec_name = 'table_id'

    date_hour = fields.Datetime('Date et Heure', default=fields.datetime.now())
    designation = fields.Char("Designations")
    artiste= fields.Many2one('res.partner',"Artistes et Titres")
    support = fields.Char("Support")
    duree  = fields.Float("Duree")
    radio_id = fields.Many2one("radio.cafrad")




class stagiaire_radio(models.Model):
    """Defining model for emsion radio camando."""
    _description = 'Les Stagiaires de la Radio au CAFRAD'
    _name = 'stagiaire.radio.cafrad'

    name = fields.Char("Nom", required=1)
    phone = fields.Char("Telephone")
    date_start = fields.Date("Date de debut du stage")
    date_end = fields.Date("Date de fin du stage")
    encadreur_id = fields.Many2one('hr.employee', "Encadre par ")
