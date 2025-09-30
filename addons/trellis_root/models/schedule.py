from odoo import models, fields, api, _
from datetime import timedelta

class TrellisSchedule(models.Model):
    _name = "trellis.schedule"
    _description = "Master Schedule"

    name = fields.Char(
        "Job",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
    )

    product_id = fields.Many2one("product.product", string="Product", required=True)
    qty = fields.Float("Quantity", required=True)
    start_date = fields.Date("Clone Date", required=True)

    cycle_type = fields.Selection([
        ("production", "Production Crop"),
        ("mother", "Mother Replenishment"),
    ], string="Cycle Type", default="production", required=True)

    # Color for Calendar/Gantt
    color = fields.Integer("Color", compute="_compute_color", store=True)

    # Computed stage dates
    veg_date = fields.Date("Veg Date", compute="_compute_stage_dates", store=True)
    flower_date = fields.Date("Flower Date", compute="_compute_stage_dates", store=True)
    harvest_date = fields.Date("Harvest Date", compute="_compute_stage_dates", store=True)
    dry_date = fields.Date("Dry Complete", compute="_compute_stage_dates", store=True)
    buck_start_date = fields.Date("Buck Start", compute="_compute_stage_dates", store=True)
    buck_date = fields.Date("Buck Complete", compute="_compute_stage_dates", store=True)

    state = fields.Selection([
        ("planned", "Planned"),
        ("released", "Released"),
    ], default="planned")

    mo_id = fields.Many2one("mrp.production", string="Manufacturing Order")

    stage_ids = fields.One2many("trellis.schedule.stage", "schedule_id", string="Stages")

    @api.depends("cycle_type")
    def _compute_color(self):
        for rec in self:
            if rec.cycle_type == "production":
                rec.color = 10  # Green
            elif rec.cycle_type == "mother":
                rec.color = 2   # Purple
            else:
                rec.color = 0   # Default grey

    @api.depends("start_date", "name", "cycle_type")
    def _compute_stage_dates(self):
        for rec in self:
            if rec.start_date:
                clone = fields.Date.from_string(rec.start_date)
                veg = clone + timedelta(days=16)

                stages = []

                if rec.cycle_type == "production":
                    flower = veg + timedelta(days=10)
                    harvest = flower + timedelta(days=65)

                    dry_start = harvest
                    dry_end = harvest + timedelta(days=14)
                    buck_start = dry_end + timedelta(days=1)
                    buck_end = buck_start + timedelta(days=3)

                    rec.veg_date = veg
                    rec.flower_date = flower
                    rec.harvest_date = harvest
                    rec.dry_date = dry_end
                    rec.buck_start_date = buck_start
                    rec.buck_date = buck_end

                    stages = [
                        ("clone", "Clone", clone, veg),
                        ("veg", "Vegetation", veg, flower),
                        ("flower", "Flower", flower, harvest),
                        ("harvest", "Harvest", harvest, harvest),
                        ("dry", "Dry", dry_start, dry_end),
                        ("buck", "Buck", buck_start, buck_end),
                    ]

                elif rec.cycle_type == "mother":
                    rec.veg_date = veg
                    rec.flower_date = rec.harvest_date = rec.dry_date = rec.buck_start_date = rec.buck_date = False

                    stages = [
                        ("clone", "Clone", clone, veg),
                        ("veg", "Vegetation", veg, veg + timedelta(days=28)),
                    ]

                rec.stage_ids = [(5, 0, 0)]
                rec.stage_ids = [(0, 0, {
                    "stage": key,
                    "name": f"{rec.name} - {label}",
                    "date_start": start,
                    "date_stop": stop,
                }) for key, label, start, stop in stages]

            else:
                rec.veg_date = rec.flower_date = rec.harvest_date = rec.dry_date = rec.buck_start_date = rec.buck_date = False
                rec.stage_ids = [(5, 0, 0)]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                product = self.env["product.product"].browse(vals.get("product_id"))
                strain_name = product.display_name if product else "Unknown"

                cycle_type = vals.get("cycle_type", "production")
                cycle_code = "PC" if cycle_type == "production" else "MR"

                clone_date = vals.get("start_date")
                date_str = clone_date.replace("-", "") if clone_date else "00000000"

                seq = self.env["ir.sequence"].next_by_code("trellis.schedule") or "000"

                vals["name"] = f"{strain_name} - {cycle_code} - {date_str} - {seq}"

        return super().create(vals_list)

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
