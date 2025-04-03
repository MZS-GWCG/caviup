# wizards/change_account_wizard.py

from odoo import api, fields, models

class ChangeAccountWizard(models.TransientModel):
    _name = 'change.account.wizard'
    _description = 'Wizard to change account in account move line'

    account_id = fields.Many2one('account.account', string='New Account', required=True)
    move_line_ids = fields.Many2many('account.move.line', string='Move Lines')

    @api.model
    def default_get(self, fields):
        res = super(ChangeAccountWizard, self).default_get(fields)
        res['move_line_ids'] = self.env.context.get('active_ids', [])
        return res

    def change_account(self):
        for line in self.move_line_ids:
            line.update({'account_id': self.account_id.id})
        return {'type': 'ir.actions.act_window_close'}


