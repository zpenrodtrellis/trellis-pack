from odoo import api, fields, models

class TrellisVaultControlledDocument(models.Model):
    _name = "trellis.vault.controlled.document"
    _description = "Controlled Document"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name, revision desc, id desc"

    name = fields.Char(required=True, tracking=True, help="Document title")
    code = fields.Char(string="Doc Code", index=True, tracking=True, help="Internal code, e.g., SOP-001")
    revision = fields.Char(default="A", required=True, tracking=True)
    previous_version_id = fields.Many2one(
        "trellis.vault.controlled.document", string="Previous Version", tracking=True
    )
    effective_date = fields.Date(tracking=True)
    owner_id = fields.Many2one("res.users", string="Owner", default=lambda self: self.env.user, tracking=True)

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("archived", "Archived"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )

    is_locked = fields.Boolean(compute="_compute_is_locked", store=False)
    training_record_count = fields.Integer(compute="_compute_training_record_count")

    # ✅ Add this line — required for attachments to appear
    attachment_ids = fields.Many2many(
        "ir.attachment", "trellis_doc_ir_attachments_rel", "doc_id", "attachment_id",
        string="Attachments"
    )

    @api.depends("state")
    def _compute_is_locked(self):
        for rec in self:
            rec.is_locked = rec.state in ("active", "archived")

    def _compute_training_record_count(self):
        data = self.env["trellis.vault.training.record"].read_group(
            [("document_id", "in", self.ids)], ["document_id"], ["document_id"]
        )
        count_map = {d["document_id"][0]: d["document_id_count"] for d in data}
        for rec in self:
            rec.training_record_count = count_map.get(rec.id, 0)

    def action_view_training_records(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Training Records",
            "res_model": "trellis.vault.training.record",
            "view_mode": "list,form",
            "domain": [("document_id", "=", self.id)],
            "context": {"default_document_id": self.id},
        }

    def action_activate(self):
        for rec in self:
            rec.state = "active"
            if not rec.effective_date:
                rec.effective_date = fields.Date.context_today(self)

    def action_archive(self):
        for rec in self:
            rec.state = "archived"

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = "draft"


compliance_log_ids = fields.One2many(
    "trellis.vault.compliance.log", "document_id", string="Compliance Logs"
)

# ADD this helper anywhere in the class
def _log_compliance(self, action: str, **kw):
    for rec in self:
        self.env["trellis.vault.compliance.log"].sudo().create({
            "document_id": rec.id,
            "action": action,
            "old_state": kw.get("old_state"),
            "new_state": kw.get("new_state"),
            "attachment_id": kw.get("attachment_id"),
            "note": kw.get("note"),
        })

# UPDATE your three state methods like so:
def action_activate(self):
    for rec in self:
        old = rec.state
        rec.state = "active"
        if not rec.effective_date:
            rec.effective_date = fields.Date.context_today(self)
        rec._log_compliance("state_change", old_state=old, new_state="active", note="Activated")

def action_archive(self):
    for rec in self:
        old = rec.state
        rec.state = "archived"
        rec._log_compliance("state_change", old_state=old, new_state="archived", note="Archived")

def action_reset_to_draft(self):
    for rec in self:
        old = rec.state
        rec.state = "draft"
        rec._log_compliance("state_change", old_state=old, new_state="draft", note="Reset to Draft")
