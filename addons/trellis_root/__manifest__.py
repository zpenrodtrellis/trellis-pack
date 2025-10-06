{
    "name": "Trellis Root",
    "version": "19.0.1.0.0",
    "author": "Trellis",
    "license": "LGPL-3",
    "depends": [
        "base",
        "product",
        "mrp",
    ],
    "data": [
        # Security
        "security/ir.model.access.csv",

        # Sequences
        "data/schedule_sequence.xml",

        # Views
        "views/schedule_view.xml",

        # Product category and cost input products
        "data/product_category.xml",
        "data/product.template.csv",   # templates for cost inputs
        "data/product_product.csv",    # variants for cost inputs

        # BoMs
        "data/mrp_bom.csv",            # BoM header
        "data/mrp_bom_line.csv",       # BoM lines
    ],
    "installable": True,
    "application": True,
}
