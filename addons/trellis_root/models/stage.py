from odoo import models, fields

class TrellisScheduleStage(models.Model):
    _name = "trellis.schedule.stage"
    _description = "Stage Event"

    schedule_id = fields.Many2one("trellis.schedule", string="Master Schedule", ondelete="cascade")
    name = fields.Char("Event", required=True)
    stage = fields.Selection([
        ("clone", "Clone"),
        ("veg", "Vegetation"),
        ("flower", "Flower"),
        ("harvest", "Harvest"),
        ("dry", "Dry"),
        ("buck", "Buck"),
    ], string="Stage", required=True)
    date = fields.Date("Date", required=True)
