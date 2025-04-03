# -*- coding: utf-8 -*-
{
    "name": "Alternative Product Base",

    "author": "Praj Technologies",

    "version": "0.0.1",

    "license": "OPL-1",

    "support": "prajtech4@gmail.com",

    "category": "Extra Tools",

    "summary": "Add Alternative Products in your Product and choose them when creating sale order, purchase order or manufacturing order",

    "description": """Alternative Products Substitute Product Replace Product""",

    "depends": ['base', 'product'],

    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",

        "wizard/alternative_wizard_views.xml",

        "views/product_product_views.xml",
    ],
    'images': ["static/description/img.png"],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 5.0,
    "currency": "EUR"
}
