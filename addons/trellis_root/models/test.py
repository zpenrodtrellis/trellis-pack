from odoo import models, fields

class TrellisTest(models.Model):
    _name = "trellis.test"
    _description = "Trellis Test Model"

    name = fields.Char(string="Name", required=True)
