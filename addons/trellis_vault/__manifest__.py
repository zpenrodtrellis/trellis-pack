{
    "name": "Trellis Vault",
    "version": "19.0.2.0.0",
    "summary": "Vault master data + controlled documents + training records",
    "author": "Trellis Systems",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",

        # base model views
        "views/strain_views.xml",
        "views/mother_tag_views.xml",

        # load all actions first (so menus can safely reference them)
        "views/controlled_document_views.xml",
        "views/training_record_views.xml",
        "views/compliance_log_views.xml",

        # finally load menu structure
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
}
