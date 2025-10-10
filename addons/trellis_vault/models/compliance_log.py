from odoo import fields, models

class VaultComplianceLog(models.Model):
    _name = "trellis.vault.compliance.log"
    _description = "Vault Compliance Log"
    _order = "create_date desc, id desc"

    document_id = fields.Many2one(
        "trellis.vault.controlled.document",
        string="Controlled Document",
        required=True,
        ondelete="cascade"
    )
    action = fields.Selection([
        ("state_change", "State Change"),
        ("attachment_add", "Attachment Added"),
        ("attachment_delete", "Attachment Deleted"),
        ("note", "Note"),
    ], required=True)
    old_state = fields.Selection([
        ("draft", "Draft"),
        ("active", "Active"),
        ("archived", "Archived"),
    ])
    new_state = fields.Selection([
        ("draft", "Draft"),
        ("active", "Active"),
        ("archived", "Archived"),
    ])
    attachment_id = fields.Many2one("ir.attachment", string="Attachment")
    user_id = fields.Many2one("res.users", string="User", default=lambda s: s.env.user, readonly=True)
    note = fields.Char(string="Details")
