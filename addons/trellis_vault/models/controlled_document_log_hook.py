from odoo import api, models

# Track these fields on write
TRACK_FIELDS_CD = ["name", "document_number", "revision", "state", "effective_date", "owner_id", "approver_id"]


class ControlledDocumentHook(models.Model):
    _inherit = "trellis.vault.controlled.document"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        reg = self.env["trellis.vault.regulatory.change"]
        for rec in records:
            reg.log_event(model=self._name, res_id=rec.id, action_type="created")
        return records

    def write(self, vals):
        reg = self.env["trellis.vault.regulatory.change"]
        before = {r.id: r.read(TRACK_FIELDS_CD)[0] for r in self}
        res = super().write(vals)
        for rec in self:
            after = rec.read(TRACK_FIELDS_CD)[0]
            changed = [f for f in TRACK_FIELDS_CD if before[rec.id].get(f) != after.get(f)]
            if changed:
                reg.log_event(
                    model=self._name,
                    res_id=rec.id,
                    action_type=self._infer_action_type_cd(before[rec.id], after),
                    changed_fields=changed,
                    old_values={f: before[rec.id].get(f) for f in changed},
                    new_values={f: after.get(f) for f in changed},
                )
        return res

    def _infer_action_type_cd(self, old, new):
        if old.get("state") != new.get("state"):
            mapping = {
                "submitted": "submitted",
                "approved": "approved",
                "effective": "published",
                "archived": "archived",
                "superseded": "superseded",
            }
            return mapping.get(new.get("state"), "updated")
        return "updated"
