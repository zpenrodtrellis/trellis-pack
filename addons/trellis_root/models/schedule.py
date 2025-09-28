from odoo import models, fields, api

class TrellisSchedule(models.Model):
    _name = "trellis.schedule"
    _description = "Master Scheduler"

    name = fields.Char(string="Job", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    qty = fields.Float(string="Quantity", default=1.0)
    start_date = fields.Date(string="Planned Date")
    state = fields.Selection(
        [("planned", "Planned"), ("released", "Released")],
        default="planned"
    )

    def action_release_mo(self):
        """Manual release → create Manufacturing Order"""
        for rec in self:
            self.env["mrp.production"].create({
                "product_id": rec.product_id.id,
                "product_qty": rec.qty,
                "date_planned_start": rec.start_date,
                "origin": rec.name,
                "bom_id": rec.product_id.bom_ids[:1].id,
            })
            rec.state = "released"
