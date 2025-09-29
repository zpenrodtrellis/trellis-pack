from odoo import models, fields, api
from datetime import timedelta

class TrellisSchedule(models.Model):
    _name = "trellis.schedule"
    _description = "Master Schedule"

    name = fields.Char("Job", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    qty = fields.Float("Quantity", required=True)
    start_date = fields.Date("Clone Date", required=True)

    # Computed stage dates (for reference only)
    veg_date = fields.Date("Veg Date", compute="_compute_stage_dates", store=True)
    flower_date = fields.Date("Flower Date", compute="_compute_stage_dates", store=True)
    harvest_date = fields.Date("Harvest Date", compute="_compute_stage_dates", store=True)
    dry_date = fields.Date("Dry Complete", compute="_compute_stage_dates", store=True)
    buck_date = fields.Date("Buck Complete", compute="_compute_stage_dates", store=True)

    state = fields.Selection([
        ("planned", "Planned"),
        ("released", "Released"),
    ], default="planned")

    mo_id = fields.Many2one("mrp.production", string="Manufacturing Order")

    stage_ids = fields.One2many("trellis.schedule.stage", "schedule_id", string="Stages")

    @api.depends("start_date", "name")
    def _compute_stage_dates(self):
        for rec in self:
            if rec.start_date:
                clone = fields.Date.from_string(rec.start_date)
                veg = clone + timedelta(days=16)
                flower = veg + timedelta(days=10)
                harvest = flower + timedelta(days=65)

                # Harvest = 1 day
                dry_start = harvest
                dry_end = harvest + timedelta(days=14)     # 2-week drying window
                buck_start = dry_end + timedelta(days=1)   # starts after drying
                buck_end = buck_start + timedelta(days=3)  # 3-day buck window

                # Assign computed fields
                rec.veg_date = veg
                rec.flower_date = flower
                rec.harvest_date = harvest
                rec.dry_date = dry_end
                rec.buck_date = buck_end

                # Build stage events
                stages = [
                    ("clone", "Clone", clone, veg),
                    ("veg", "Vegetation", veg, flower),
                    ("flower", "Flower", flower, harvest),
                    ("harvest", "Harvest", harvest, harvest),      # single day
                    ("dry", "Dry", dry_start, dry_end),            # 2 weeks
                    ("buck", "Buck", buck_start, buck_end),        # 3 days
                ]

                rec.stage_ids = [(5, 0, 0)]  # clear existing
                rec.stage_ids = [(0, 0, {
                    "stage": key,
                    "name": f"{rec.name} - {label}",
                    "date_start": start,
                    "date_stop": stop,
                }) for key, label, start, stop in stages]

            else:
                rec.veg_date = rec.flower_date = rec.harvest_date = rec.dry_date = rec.buck_date = False
                rec.stage_ids = [(5, 0, 0)]

    def action_release_mo(self):
        for rec in self:
            mo = self.env["mrp.production"].create({
                "product_id": rec.product_id.id,
                "product_qty": rec.qty,
                "date_start": rec.start_date,
            })
            rec.mo_id = mo.id
            rec.state = "released"
        return True

    def open_mo(self):
        self.ensure_one()
        if self.mo_id:
            return {
                "type": "ir.actions.act_window",
                "res_model": "mrp.production",
                "view_mode": "form",
                "res_id": self.mo_id.id,
            }
        return False
