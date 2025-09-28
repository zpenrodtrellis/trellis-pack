from odoo import models, fields, api

class TrellisSchedule(models.Model):
    _name = "trellis.schedule"
    _description = "Master Schedule"

    name = fields.Char("Job", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    qty = fields.Float("Quantity", required=True)
    start_date = fields.Date("Planned Date", required=True)
    state = fields.Selection([
        ("planned", "Planned"),
        ("released", "Released"),
    ], default="planned")
    mo_id = fields.Many2one("mrp.production", string="Manufacturing Order")

    def action_release_mo(self):
        for rec in self:
            mo = self.env["mrp.production"].create({
                "product_id": rec.product_id.id,
                "product_qty": rec.qty,
                "date_start": rec.start_date,   # ✅ corrected field
            })
            rec.mo_id = mo.id
            rec.state = "released"
