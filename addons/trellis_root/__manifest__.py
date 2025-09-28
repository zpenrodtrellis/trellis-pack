{
    "name": "Trellis Root",
    "version": "19.0.1.0.0",
    "author": "Trellis",
    "depends": ["base", "mrp", "calendar"],
    "data": [
        "views/root_menu.xml",
        "views/schedule_view.xml",
        "security/ir.model.access.csv",  # load after model exists
    ],
    "installable": True,
    "application": True,
}
