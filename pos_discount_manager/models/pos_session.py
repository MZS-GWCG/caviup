from odoo import models, fields

class PosSession(models.Model):
    _inherit = "pos.session"

    def _check_employee_discount(self, employee, discount):
        """Check if employee is exceeding their allowed discount limit"""
        if employee.limited_discount and discount > employee.limited_discount:
            return False  # Discount exceeds allowed limit
        return True
