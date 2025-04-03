{
    "name": "Product Image Editor Access",
    "version": "18.0.1.0.0",
    "category": "Product",
    "summary": "Restrict and manage access to product images.",
    "author": "GW",
    "license": "LGPL-3",
    "depends": ["product"],
    "data": [
        "security/product_image_rule.xml",  # 👈 Load groups first
        "security/ir.model.access.csv",  # 👈 Load access rights after
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
