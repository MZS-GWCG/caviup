# -*- coding: utf-8 -*-
{
    "name": "Sale Alternative Product",

    "author": "Praj Technologies",

    "version": "0.0.1",

    "license": "OPL-1",

    "support": "prajtech4@gmail.com",

    "category": "Extra Tools",

    "summary": "Sale Order Alternative Products in your Product and choose them when creating sale order, purchase order or manufacturing order",

    "description": """Sale Alternative Products Substitute Product Replace Product Sale Order Alternative""",

    "depends": ['base', 'pt_alternative_base', 'sale_management', 'stock'],

    "data": [
        "wizard/inherit_sale_alternative_wizard.xml",
        "views/sale_order_line_views.xml",
    ],
    'images': ["static/description/img.png"],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 11.0,
    "currency": "EUR"
}
