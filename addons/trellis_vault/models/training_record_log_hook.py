from odoo import api, models

# Track these fields on write
TRACK_FIELDS_TR = ["trainee_id", "course_id", "status", "assigned_date", "completed_date", "due_date"]


class TrainingRecordHook(models.Model):
    _inherit = "trellis.vault.training.record"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        reg = self.env["trellis.vault.regulatory.change"]
        for rec in records:
            reg.log_event(model=self._name, res_id=rec.id, action_type="training_assigned")
        return records

    def write(self, vals):
        reg = self.env["trellis.vault.regulatory.change"]
        before = {r.id: r.read(TRACK_FIELDS_TR)[0] for r in self}
        res = super().write(vals)
        for rec in self:
            after = rec.read(TRACK_FIELDS_TR)[0]
            changed = [f for f in TRACK_FIELDS_TR if before[rec.id].get(f) != after.get(f)]
            if changed:
                action = "training_completed" if ("completed_date" in changed and after.get("completed_date")) else "updated"
                reg.log_event(
                    model=self._name,
                    res_id=rec.id,
                    action_type=action,
                    changed_fields=changed,
                    old_values={f: before[rec.id].get(f) for f in changed},
                    new_values={f: after.get(f) for f in changed},
                )
        return res
