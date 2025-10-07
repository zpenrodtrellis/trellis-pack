from odoo import models, fields

class TrellisVaultMotherTag(models.Model):
    _name = "trellis.vault.mother.tag"
    _description = "Mother Tags"

    name = fields.Char(string="Mother Name", required=True)
    strain_id = fields.Many2one("trellis.vault.strain", string="Strain")
    tag_number = fields.Char(string="METRC Tag")
