{
    "name": "POS Discount Manager",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Manage discount limits for employees in POS.",
    "author": "Your Company",
    "license": "LGPL-3",
    "depends": ["point_of_sale", "hr"],
    "data": [
        "views/hr_employee_views.xml",
        "security/ir.model.access.csv"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
