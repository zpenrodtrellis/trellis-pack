from odoo import api, models

class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for att, vals in zip(records, vals_list):
            if att.res_model == "trellis.vault.controlled.document" and att.res_id:
                self.env["trellis.vault.compliance.log"].sudo().create({
                    "document_id": att.res_id,
                    "action": "attachment_add",
                    "attachment_id": att.id,
                    "note": att.name or "Attachment Added",
                })
        return records

    def unlink(self):
        for att in self:
            if att.res_model == "trellis.vault.controlled.document" and att.res_id:
                self.env["trellis.vault.compliance.log"].sudo().create({
                    "document_id": att.res_id,
                    "action": "attachment_delete",
                    "attachment_id": att.id,
                    "note": att.name or "Attachment Deleted",
                })
        return super().unlink()
