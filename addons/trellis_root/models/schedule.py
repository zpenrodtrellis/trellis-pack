from odoo import models, fields, api
from datetime import timedelta

class TrellisSchedule(models.Model):
    _name = "trellis.schedule"
    _description = "Trellis Master Schedule"

    name = fields.Char("Job", required=True)
    product_id = fields.Many2one("product.product", string="Product")
    qty = fields.Float("Quantity")
    start_date = fields.Date("Planned Date")
    state = fields.Selection(
        [("planned", "Planned"), ("released", "Released")],
        default="planned",
    )
    mo_id = fields.Many2one("mrp.production", string="Manufacturing Order")

    # Computed stage dates
    clone_date = fields.Date("Clone Date", compute="_compute_stage_dates", store=True)
    veg_date = fields.Date("Veg Date", compute="_compute_stage_dates", store=True)
    flower_date = fields.Date("Flower Date", compute="_compute_stage_dates", store=True)
    harvest_date = fields.Date("Harvest Date", compute="_compute_stage_dates", store=True)
    dry_date = fields.Date("Dry Date", compute="_compute_stage_dates", store=True)
    buck_date = fields.Date("Buck Date", compute="_compute_stage_dates", store=True)

    # Computed display name for Gantt/Calendar
    display_name_stage = fields.Char("Stage Label", compute="_compute_display_name_stage")

    @api.depends("start_date")
    def _compute_stage_dates(self):
        """Compute dates for each stage based on starting clone date."""
        for rec in self:
            if rec.start_date:
                rec.clone_date = rec.start_date
                rec.veg_date = rec.start_date + timedelta(days=16)
                rec.flower_date = rec.veg_date + timedelta(days=10)
                rec.harvest_date = rec.flower_date + timedelta(days=65)
                rec.dry_date = rec.harvest_date + timedelta(days=10)
                rec.buck_date = rec.dry_date + timedelta(days=5)
            else:
                rec.clone_date = rec.veg_date = rec.flower_date = False
                rec.harvest_date = rec.dry_date = rec.buck_date = False

    @api.depends("name", "clone_date", "veg_date", "flower_date", "harvest_date", "dry_date", "buck_date")
    def _compute_display_name_stage(self):
        """Generate stage-specific labels for Gantt/Calendar views."""
        for rec in self:
            if rec.clone_date:
                rec.display_name_stage = f"{rec.name} - Clone"
            elif rec.veg_date:
                rec.display_name_stage = f"{rec.name} - Veg"
            elif rec.flower_date:
                rec.display_name_stage = f"{rec.name} - Flower"
            elif rec.harvest_date:
                rec.display_name_stage = f"{rec.name} - Harvest"
            elif rec.dry_date:
                rec.display_name_stage = f"{rec.name} - Dry"
            elif rec.buck_date:
                rec.display_name_stage = f"{rec.name} - Buck"
            else:
                rec.display_name_stage = rec.name

    def action_release_mo(self):
        """Release Manufacturing Order from schedule."""
        for rec in self:
            if rec.state != "released":
                mo = self.env["mrp.production"].create({
                    "product_id": rec.product_id.id,
                    "product_qty": rec.qty,
                    "date_start": rec.start_date,
                    "origin": rec.name,
                })
                rec.mo_id = mo.id
                rec.state = "released"
