{
    "name": "Trellis Root",
    "version": "19.0.1.0.0",
    "author": "Trellis",
    "license": "LGPL-3",
    "depends": ["base", "product", "mrp"],
    "data": [
        "security/ir.model.access.csv",
        "data/schedule_sequence.xml",
        "views/schedule_view.xml",
        "data/product_category.xml",
        "data/product_product.csv",
        "data/mrp_bom.csv",
        "data/mrp_bom_line.csv",
    ],
    "installable": True,
    "application": True,
}
