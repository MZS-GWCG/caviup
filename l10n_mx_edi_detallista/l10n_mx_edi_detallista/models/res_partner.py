# coding: utf-8

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_mx_edi_detallista = fields.Boolean(
        'Complemento Detallista?', help='check this box to add by default '
        'the Detallista complement in invoices for this customer.')
