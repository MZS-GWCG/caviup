from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    limited_discount = fields.Float(string="Limited Discount", help="Maximum discount an employee can apply in POS")
