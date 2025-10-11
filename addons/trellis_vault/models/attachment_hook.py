from odoo import api, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        reg = self.env["trellis.vault.regulatory.change"]
        allowed = [m[0] for m in reg.ALLOWED_MODELS]
        for rec in records:
            if rec.res_model in allowed and rec.res_id:
                reg.log_event(
                    model=rec.res_model,
                    res_id=rec.res_id,
                    action_type="attachment_added",
                    note=f"Attachment added: {rec.name}",
                )
        return records

    def unlink(self):
        reg = self.env["trellis.vault.regulatory.change"]
        allowed = [m[0] for m in reg.ALLOWED_MODELS]
        for rec in self:
            if rec.res_model in allowed and rec.res_id:
                reg.log_event(
                    model=rec.res_model,
                    res_id=rec.res_id,
                    action_type="attachment_removed",
                    note=f"Attachment removed: {rec.name}",
                )
        return super().unlink()
