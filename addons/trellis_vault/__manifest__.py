{
    "name": "Trellis Vault",
    "version": "19.0.2.0.0",
    "summary": "Vault master data + controlled documents + training records",
    "author": "Trellis Systems",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/strain_views.xml",
        "views/mother_tag_views.xml",
        "views/controlled_document_views.xml",  # must load before menus
        "views/training_record_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
}
