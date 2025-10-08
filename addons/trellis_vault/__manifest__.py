{
    "name": "Trellis Vault",
    "version": "19.0.2.0.0",
    "summary": "Vault master data + controlled documents + training records",
    "author": "Trellis Systems",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        # existing views (keep)
        "views/strain_views.xml",
        "views/mother_tag_views.xml",
        "views/menus.xml",
        # NEW controlled docs
        "views/controlled_document_views.xml",
        "views/training_record_views.xml",
    ],
    "installable": True,
    "application": False,
}
