# -*- coding: utf-8 -*-
# Part of Praj Technologies.

from odoo import models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def action_open_alternative_wizard(self):
        return {
            'name':'Alternative Products',
            'res_model': 'pt.alternative.wizard',
            'view_mode':'form',
            'view_id':self.env.ref('pt_alternative_base.pt_alternative_wizard_form').id,
            'target':'new',
            'type':'ir.actions.act_window',
            'context' : {
                'default_alternative_product_ids' : self.product_id.pt_alternative_product_ids.ids,
            }
        }