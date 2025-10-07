from odoo import api, fields, models

class TrellisVaultStrain(models.Model):
    _name = "trellis.vault.strain"
    _description = "Strain (Vault Master)"

    name = fields.Char(required=True, index=True)
    code = fields.Char(help="Short code for the strain, e.g., BD")
    default_mother_tag_prefix = fields.Char(help="e.g., MOM-BD")
    active = fields.Boolean(default=True)
    note = fields.Text()
    mother_tag_count = fields.Integer(
        compute="_compute_mother_tag_count",
        store=False,
        help="Number of mother tags linked to this strain",
    )

    @api.depends('id')
    def _compute_mother_tag_count(self):
        groups = self.env['trellis.vault.mother.tag'].read_group(
            [('strain_id', 'in', self.ids)],
            fields=['strain_id'],
            groupby=['strain_id']
        )
        counts = {g['strain_id'][0]: g['strain_id_count'] for g in groups if g.get('strain_id')}
        for rec in self:
            rec.mother_tag_count = counts.get(rec.id, 0)
