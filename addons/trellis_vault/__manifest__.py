{
    "name": "Trellis Vault",
    "version": "19.0.2.0.0",
    "summary": "Vault master data + controlled documents + training records + regulatory change history",
    "author": "Trellis Systems",
    "license": "LGPL-3",
    "depends": ["base", "mail", "web"],
    "data": [
        # --- your existing assets from the ZIP ---
        "security/ir.model.access.csv",
        "views/strain_views.xml",
        "views/mother_tag_views.xml",
        "views/controlled_document_views.xml",
        "views/training_record_views.xml",
        "views/menus.xml",

        # --- NEW: Regulatory Change History (additive only) ---
        "security/security.xml",
        "security/ir.model.access.regulatory.csv",
        "views/regulatory_change_views.xml",
        "views/regulatory_change_menu.xml",
        "report/regulatory_change_report.xml",
        "report/regulatory_change_templates.xml",
    ],
    "installable": True,
    "application": False,
}
