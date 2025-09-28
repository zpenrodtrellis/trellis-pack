from odoo import models, fields, api
from datetime import timedelta

class TrellisSchedule(models.Model):
    _name = "trellis.schedule"
    _description = "Master Schedule"

    name = fields.Char("Job", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    qty = fields.Float("Quantity", required=True)
    start_date = fields.Date("Clone Date", required=True)

    # Stage dates (computed)
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

    @api.depends("start_date")
    def _compute_stage_dates(self):
        for rec in self:
            if rec.start_date:
                clone = fields.Date.from_string(rec.start_date)

                veg = clone + timedelta(days=16)
                flower = veg + timedelta(days=10)
                harvest = flower + timedelta(days=65)
                dry = harvest + timedelta(days=10)
                buck = dry  # later adjust to align to Friday if needed

                rec.veg_date = veg
                rec.flower_date = flower
                rec.harvest_date = harvest
                rec.dry_date = dry
                rec.buck_date = buck

                # sync child stage records
                stages = [
                    ("clone", "Clone", clone),
                    ("veg", "Vegetation", veg),
                    ("flower", "Flower", flower),
                    ("harvest", "Harvest", harvest),
                    ("dry", "Dry", dry),
                    ("buck", "Buck", buck),
                ]
                Stage = self.env["trellis.schedule.stage"]
                Stage.search([("schedule_id", "=", rec.id)]).unlink()
                for key, label, date in stages:
                    Stage.create({
                        "schedule_id": rec.id,
                        "stage": key,
                        "name": f"{rec.name} - {label}",
                        "date": date,
                    })
            else:
                rec.veg_date = rec.flower_date = rec.harvest_date = rec.dry_date = rec.buck_date = False
                rec.stage_ids.unlink()

    def action_release_mo(self):
        for rec in self:
            mo = self.env["mrp.production"].create({
                "product_id": rec.product_id.id,
                "product_qty": rec.qty,
                "date_start": rec.start_date,  # Odoo 19 field
            })
            rec.mo_id = mo.id
            rec.state = "released"
