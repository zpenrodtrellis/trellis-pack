from odoo import models, fields, api
from datetime import timedelta

class TrellisSchedule(models.Model):
    _name = "trellis.schedule"
    _description = "Master Schedule"

    name = fields.Char("Job", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    qty = fields.Float("Quantity", required=True)
    start_date = fields.Date("Clone Date", required=True)

    # Stage dates (still computed for later use, but Calendar only uses Clone for now)
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

    @api.depends("start_date")
    def _compute_stage_dates(self):
        for rec in self:
            if rec.start_date:
                clone = fields.Date.from_string(rec.start_date)
                veg = clone + timedelta(days=16)
                flower = veg + timedelta(days=10)
                harvest = flower + timedelta(days=65)
                dry = harvest + timedelta(days=10)
                buck = dry

                rec.veg_date = veg
                rec.flower_date = flower
                rec.harvest_date = harvest
                rec.dry_date = dry
                rec.buck_date = buck
            else:
                rec.veg_date = rec.flower_date = rec.harvest_date = rec.dry_date = rec.buck_date = False

    def action_release_mo(self):
        for rec in self:
            mo = self.env["mrp.production"].create({
                "product_id": rec.product_id.id,
                "product_qty": rec.qty,
                "date_start": rec.start_date,
            })
            rec.mo_id = mo.id
            rec.state = "released"

    def name_get(self):
        """Minimal display: always append - Clone."""
        result = []
        for record in self:
            display = f"{record.name} - Clone"
            result.append((record.id, display))
        return result
