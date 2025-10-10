{
    "name": "Trellis Vault",
    "version": "19.0.2.0.0",
    "summary": "Vault master data + controlled documents + training records",
    "author": "Trellis Systems",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",

        # base model views (no action refs)
        "views/strain_views.xml",
        "views/mother_tag_views.xml",

        # make sure the Compliance Log action exists BEFORE any form uses it
        "views/compliance_log_views.xml",

        # now load forms that reference that action id
        "views/controlled_document_views.xml",
        "views/training_record_views.xml",

        # menus always last
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
}
