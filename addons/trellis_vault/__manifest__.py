{
    "name": "Trellis Vault",
    "version": "19.0.2.0.0",
    "summary": "Vault master data + controlled documents + training records",
    "author": "Trellis Systems",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",

        # base models' views (no cross-refs)
        "views/strain_views.xml",
        "views/mother_tag_views.xml",

        # MENUS FIRST so children can attach
        "views/menus.xml",

        # define Compliance Log action BEFORE form smart-button references it
        "views/compliance_log_views.xml",

        # now forms that reference that action
        "views/controlled_document_views.xml",
        "views/training_record_views.xml",
    ],
    "installable": True,
    "application": False,
}
