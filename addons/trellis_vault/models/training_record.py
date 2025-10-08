from odoo import fields, models

class TrellisVaultTrainingRecord(models.Model):
    _name = "trellis.vault.training.record"
    _description = "Training Record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "training_date desc, id desc"

    name = fields.Char(required=True, default="Training", tracking=True)
    document_id = fields.Many2one("trellis.vault.controlled.document", required=True, ondelete="cascade", tracking=True)
    trainee_id = fields.Many2one("res.users", string="Trainee", required=True, default=lambda self: self.env.user, tracking=True)
    trainer_id = fields.Many2one("res.users", string="Trainer", tracking=True)
    training_date = fields.Date(required=True, default=fields.Date.context_today, tracking=True)

    state = fields.Selection(
        [("draft", "Draft"), ("completed", "Completed"), ("locked", "Locked")],
        default="draft",
        required=True,
        tracking=True,
    )

    # Simple e-sign placeholders (expand later with Stream)
    signed_by_id = fields.Many2one("res.users", string="Signed By", tracking=True, readonly=True)
    signed_on = fields.Datetime(string="Signed On", tracking=True, readonly=True)

    def action_complete(self):
        for rec in self:
            rec.state = "completed"

    def action_sign_and_lock(self):
        for rec in self:
            rec.signed_by_id = self.env.user
            rec.signed_on = fields.Datetime.now()
            rec.state = "locked"

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = "draft"
            rec.signed_by_id = False
            rec.signed_on = False
