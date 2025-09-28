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
    mo_id = fields.Many2one("mrp.production", string="Manufacturing Order", readonly=True)

    def action_release_mo(self):
        """Create a Manufacturing Order from this schedule line"""
        for rec in self:
            mo = self.env["mrp.production"].create({
                "product_id": rec.product_id.id,
                "product_qty": rec.qty,
                "date_planned_start": rec.start_date or fields.Date.today(),
                "bom_id": rec.product_id.bom_ids[:1].id,  # use first BOM if exists
            })
            rec.mo_id = mo.id
            rec.state = "released"
        return True
