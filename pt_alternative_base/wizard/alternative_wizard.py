# -*- coding: utf-8 -*-
# Part of Praj Technologies.

from odoo import fields, models

class AlternativeSelection(models.TransientModel):
    _name = 'pt.alternative.wizard'
    _description = "Displays all the alternative products"

    change_product_id = fields.Many2one(
        'product.product', string="Active Product")
    alternative_product_ids = fields.Many2many(
        'product.product', string="Alternate Products")
    
    def update_product(self):
        pass