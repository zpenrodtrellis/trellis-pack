from odoo import api, fields, models, _
from odoo.exceptions import UserError
import json


class RegulatoryChange(models.Model):
    _name = "trellis.vault.regulatory.change"
    _description = "Regulatory Change History"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc, id desc"

    # Both models from your ZIP are tracked; nothing else.
    ALLOWED_MODELS = [
        ("trellis.vault.controlled.document", "Controlled Document"),
        ("trellis.vault.training.record", "Training Record"),
    ]

    name = fields.Char(string="Summary", compute="_compute_name", store=True)
    date = fields.Datetime(default=lambda self: fields.Datetime.now(), required=True, index=True)
    user_id = fields.Many2one("res.users", default=lambda self: self.env.user, required=True)
    action_type = fields.Selection([
        ("created", "Created"),
        ("updated", "Updated"),
        ("submitted", "Submitted for Approval"),
        ("approved", "Approved"),
        ("published", "Published/Effective"),
        ("superseded", "Superseded"),
        ("archived", "Archived"),
        ("training_assigned", "Training Assigned"),
        ("training_completed", "Training Completed"),
        ("attachment_added", "Attachment Added"),
        ("attachment_removed", "Attachment Removed"),
        ("note", "Note"),
    ], required=True, index=True)

    related_ref = fields.Reference(selection=ALLOWED_MODELS, string="Related Record", required=True, index=True)
    changed_fields = fields.Char(help="Comma-separated field names that changed")
    old_values = fields.Text(string="Old Values (JSON)")
    new_values = fields.Text(string="New Values (JSON)")
    note = fields.Text()
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    # Immutable after creation (except system admin)
    def write(self, vals):
        if not self.env.is_superuser() and not self.env.user.has_group("base.group_system"):
            blocked = set(vals) - {"message_follower_ids", "message_partner_ids", "message_ids", "activity_ids"}
            if blocked:
                raise UserError(_("Regulatory Change History entries are immutable. Create a new note instead."))
        return super().write(vals)

    def unlink(self):
        if not self.env.is_superuser() and not self.env.user.has_group("base.group_system"):
            raise UserError(_("Deletion is not allowed for Regulatory Change History entries."))
        return super().unlink()

    @api.depends("action_type", "related_ref")
    def _compute_name(self):
        for rec in self:
            target = rec.related_ref.display_name if rec.related_ref else ""
            rec.name = f"{target} — {dict(self._fields['action_type'].selection).get(rec.action_type, '')}"

    # Helper used by hooks
    @api.model
    def log_event(self, *, model, res_id, action_type,
                  changed_fields=None, old_values=None, new_values=None, note=None):
        allowed = [m[0] for m in self.ALLOWED_MODELS]
        if model not in allowed:
            return  # ignore unknown models; KISS
        vals = {
            "action_type": action_type,
            "related_ref": f"{model},{res_id}",
            "changed_fields": ",".join(changed_fields or []),
            "old_values": json.dumps(old_values or {}, default=str),
            "new_values": json.dumps(new_values or {}, default=str),
            "note": note or "",
        }
        return self.sudo().create(vals)
