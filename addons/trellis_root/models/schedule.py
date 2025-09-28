from odoo import models, fields

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
