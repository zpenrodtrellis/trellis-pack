{
    "name": "Trellis Vault",
    "version": "19.0.1.0.0",
    "summary": "Master data for strains and mother tags (Vault)",
    "author": "Trellis Systems",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/strain_views.xml",
        "views/mother_tag_views.xml",
        "views/menus.xml",
        "data/trellis.vault.strain.csv",
        "data/trellis.vault.mother.tag.csv",
    ],
    "installable": True,
    "application": False,
}
