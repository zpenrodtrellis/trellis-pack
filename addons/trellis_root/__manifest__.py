{
    "name": "Trellis Root",
    "version": "19.0.1.0.0",
    "author": "Trellis",
    "license": "LGPL-3",
    "depends": ["base", "product", "mrp"],  # now includes Manufacturing
    "data": [
        "security/ir.model.access.csv",
        "data/schedule_sequence.xml",
        "views/schedule_view.xml",
        'data/production_crop_products.csv',
        'data/production_crop_bom.csv',
        'data/production_crop_bom_lines.csv',
    ],
    "installable": True,
    "application": True,
}
