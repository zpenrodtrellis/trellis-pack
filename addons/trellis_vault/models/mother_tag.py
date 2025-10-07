from odoo import fields, models

class TrellisVaultMotherTag(models.Model):
    _name = "trellis.vault.mother.tag"
    _description = "Mother Tag (Vault Master)"
    _order = "strain_id, name"

    # For now, 'name' holds the METRC tag number (can rename to 'metrc_tag' later)
    name = fields.Char(required=True, index=True, help="METRC tag or mother tag code")
    strain_id = fields.Many2one(
        "trellis.vault.strain",
        required=True,
        index=True,
        ondelete="cascade",
        help="Strain this mother tag belongs to"
    )
    group_no = fields.Integer(help="Bucket of 100 for downstream logic (1=1–100, 2=101–200, etc.)")
    active = fields.Boolean(default=True)
