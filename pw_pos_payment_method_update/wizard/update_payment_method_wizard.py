# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class UpdatePaymentMethodWizard(models.TransientModel):
    _name = "update.payment.method.wizard"
    _description = "Update Payment Method Wizard"

    pos_payment_id = fields.Many2one('pos.payment', string="Payment", readonly=True)
    payment_method_ids = fields.Many2many('pos.payment.method', compute='_compute_pos_payment_methods_ids')
    payment_method_id = fields.Many2one('pos.payment.method', string="Payment Method", required=True)

    def _compute_pos_payment_methods_ids(self):
        for wizard in self:
            wizard.payment_method_ids = wizard.pos_payment_id.session_id.config_id.payment_method_ids.ids

    @api.model
    def default_get(self, fields):
        res = super(UpdatePaymentMethodWizard, self).default_get(fields)
        payment = self.env['pos.payment'].browse(self.env.context.get('active_id'))
        res['payment_method_ids'] = payment.session_id.config_id.payment_method_ids
        return res

    def update_payment_method(self):
        if self.pos_payment_id and self.payment_method_id:
            if self.pos_payment_id.pos_order_id.state not in ('paid' ,'invoiced'):
                raise ValidationError(_('You can update only paid orders'))
            if self.payment_method_id.split_transactions and not self.pos_payment_id.pos_order_id.partner_id:
                raise ValidationError(_('You have enabled the "Identify Customer" option for Customer Account payment method,but the order %s does not contain a customer.' % self.pos_payment_id.pos_order_id.name))
            self.pos_payment_id.sudo().write({'payment_method_id': self.payment_method_id.id})
