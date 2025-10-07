from odoo import models, fields

class TrellisVaultStrain(models.Model):
    _name = "trellis.vault.strain"
    _description = "Strain Master"

    name = fields.Char(string="Strain Name", required=True)
    description = fields.Text(string="Description")
