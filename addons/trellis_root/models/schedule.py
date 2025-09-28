from odoo import models, fields, api
from datetime import timedelta

class TrellisSchedule(models.Model):
    _name = "trellis.schedule"
    _description = "Master Schedule"

    name = fields.Char("Job", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    qty = fields.Float("Quantity", required=True)
    start_date = fields.Date("Clone Date", required=True)

    stage_ids = fields.One2many("trellis.schedule.stage", "schedule_id", string="Stages")

    state = fields.Selection([
        ("planned", "Planned"),
        ("released", "Released"),
    ], default="planned")

    mo_id = fields.Many2one("mrp.production", string="Manufacturing Order")

    @api.onchange("start_date", "name")
    def _generate_stages(self):
        """Auto-create or update stage lines when start_date changes."""
        for rec in self:
            if not rec.start_date:
                rec.stage_ids = [(5, 0, 0)]  # clear stages
                continue

            base = fields.Date.from_string(rec.start_date)

            stages = [
                ("Clone", base, base + timedelta(days=16)),
                ("Veg", base + timedelta(days=16), base + timedelta(days=26)),
                ("Flower", base + timedelta(days=26), base + timedelta(days=91)),
                ("Dry", base + timedelta(days=91), base + timedelta(days=101)),
            ]

            # Buck = Friday before next Monday after Dry
            dry_end = base + timedelta(days=101)
            next_monday = dry_end + timedelta(days=(7 - dry_end.weekday()) % 7)
            buck_friday = next_monday - timedelta(days=3)
            stages.append(("Buck", dry_end, buck_friday))

            stage_vals = []
            for stage_name, start, stop in stages:
                stage_vals.append((0, 0, {
                    "name": f"{rec.name} – {stage_name}",
                    "stage_type": stage_name.lower(),
                    "date_start": start,
                    "date_stop": stop,
                }))

            rec.stage_ids = [(5, 0, 0)] + stage_vals

    def action_release_mo(self):
        for rec in self:
            mo = self.env["mrp.production"].create({
                "product_id": rec.product_id.id,
                "product_qty": rec.qty,
                "date_start": rec.start_date,
            })
            rec.mo_id = mo.id
            rec.state = "released"


class TrellisScheduleStage(models.Model):
    _name = "trellis.schedule.stage"
    _description = "Schedule Stage"

    name = fields.Char("Stage", required=True)
    stage_type = fields.Selection([
        ("clone", "Clone"),
        ("veg", "Veg"),
        ("flower", "Flower"),
        ("dry", "Dry"),
        ("buck", "Buck"),
    ], required=True)
    date_start = fields.Date("Start Date", required=True)
    date_stop = fields.Date("End Date", required=True)

    schedule_id = fields.Many2one("trellis.schedule", string="Job", ondelete="cascade")
