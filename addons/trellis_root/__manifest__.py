{
    "name": "Trellis Root",
    "version": "19.0.1.0.0",
    "author": "Trellis",
    "license": "LGPL-3",
    "depends": ["base", "product"],  # add product for Many2one field
    "data": [
        "security/ir.model.access.csv",
        "views/schedule_view.xml",
    ],
    "installable": True,
    "application": True,
}
