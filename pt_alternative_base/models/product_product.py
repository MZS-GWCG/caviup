# -*- coding: utf-8 -*-
# Part of Praj Technologies.

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    pt_alternative_product_ids = fields.Many2many('product.product','pt_product_alternative_rel','product_id','alternative_id',string="Alternative Products")