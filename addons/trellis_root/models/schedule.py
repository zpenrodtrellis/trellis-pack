from odoo import models, fields

class TrellisSchedule(models.Model):
    _name = "trellis.schedule"
    _description = "Master Scheduler"

    name = fields.Char(string="Job", required=True)
    notes = fields.Text(string="Notes")
