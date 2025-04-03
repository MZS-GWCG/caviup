from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    addenda_verify = fields.Char(related="partner_id.l10n_mx_edi_addenda.name", required=True)
    liverpool_purchase_reference = fields.Char('Número de pedido Comprador', required=True)
    liverpool_purchase_reference_date = fields.Date('Fecha de pedido Comprador', default=lambda self: fields.Datetime.now(), required=True)
    additional_reference_identification = fields.Char('Número de referencia adicional', required=True)
    delivery_note_reference = fields.Char('Número de contra-recibo', required=True)
    delivery_note_date = fields.Date('Fecha de Recepción', default=lambda self: fields.Datetime.now(), required=True)
    person_or_department_name = fields.Char('Contacto de compras: No. o Nombre de departamento Liverpool', required=True)
    alternate_party_identifaction = fields.Char('Número de emisor(proveedor)', required=True, default='0000950000442')
    special_services_type = fields.Selection(
        selection=[
            ('AJ', 'Ajustes'),
            ('CAC', 'Descuento en efectivo'),
            ('COD', 'Efectivo a la entrega'),
            ('EAB', 'Descuento por pronto pago'),
            ('FC', 'Costes del flete'),
            ('FI', 'Costes financieros'),
            ('HD', 'Manipulado'),
            ('QD', 'Descuento por cantidad'),
            ('AA', 'Abono por publicidad'),
            ('ADS', 'Pedido de un pallet completo'),
            ('ADT', 'Recogida')],
        required=False,
        copy=False,
        default='AJ',
        string="Tipo de descuento o cargo"
    )
    settlementType = fields.Selection(
        selection=[
            ('BILL_BACK', 'BILL_BACK'),
            ('OFF_INVOICE', 'OFF_INVOICE')
        ],
        required=False,
        copy=False,
        default='OFF_INVOICE',
        string="Imputación de descuento o cargo"
    )
    additional_reference_identification_type = fields.Selection(
        selection=[
            ('AAE', 'Cuenta Predial'),
            ('CK', 'Número de Cheque'),
            ('ACE', 'Número de documento(Remisión)'),
            ('ATZ', 'Número de Aprobación'),
            ('AWR', 'Número de documento que se reemplaza'),
            ('ON', 'Número de pedido(comprador)'),
            ('DQ', 'Folio de recibo de mercancías'),
            ('IV', 'Número de Factura')
        ],
        required=False,
        copy=False,
        string="Identficador de referencia adicional"
    )

    def amount_to_text(self, amount_total):
        self.ensure_one()
        currency = self.currency_id.name.upper()
        # M.N. = Moneda Nacional (National Currency)
        # M.E. = Moneda Extranjera (Foreign Currency)
        currency_type = 'M.N' if currency == 'MXN' else 'M.E.'
        # Split integer and decimal part
        amount_i, amount_d = divmod(amount_total, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(round(amount_d * 100, 2))
        words = self.currency_id.with_context(
            lang=self.company_id.partner_id.lang or 'es_ES').amount_to_text(
                amount_i).upper()
        invoice_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
            words=words, amount_d=amount_d, curr_t=currency_type)
        return invoice_words
