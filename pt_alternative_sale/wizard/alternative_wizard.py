# -*- coding: utf-8 -*-
# Part of Praj Technologies.

from odoo import models

class AlternativeSelection(models.TransientModel):
    _inherit = 'pt.alternative.wizard'
    _description = "Displays all the alternative products"

    def update_product(self):
        res = super(AlternativeSelection,self).update_product()
        if self.env.context.get('active_model') == 'sale.order.line':
            sale_order_line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
            sale_order_line.write({
                'product_id' : self.change_product_id.id,
                'price_unit' : sale_order_line.order_id.pricelist_id._get_product_price(self.change_product_id, sale_order_line.product_uom_qty)
            })
        return res