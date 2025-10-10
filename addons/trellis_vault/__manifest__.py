{
    "name": "Trellis Vault",
    "version": "19.0.2.0.0",
    "summary": "Vault master data + controlled documents + training records + compliance logs",
    "author": "Trellis Systems",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        # 1️⃣ Security (always first)
        "security/ir.model.access.csv",

        # 2️⃣ Base models / master data
        "views/strain_views.xml",
        "views/mother_tag_views.xml",

        # 3️⃣ Core feature actions & views
        "views/controlled_document_views.xml",
        "views/training_record_views.xml",

        # 4️⃣ Parent menus (Vault + Quality & Docs)
        "views/menus.xml",

        # 5️⃣ Extended features (child menus / cross-links)
        "views/compliance_log_views.xml",
    ],
    "installable": True,
    "application": False,
}
