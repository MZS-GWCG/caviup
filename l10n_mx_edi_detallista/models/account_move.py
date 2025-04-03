# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tools.profiler import QwebTracker
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.sql import column_exists, create_column
from lxml import etree
from lxml.objectify import fromstring

import logging
import logging.config

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },    
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

_logger = logging.getLogger(__name__)

class IrQWeb(models.AbstractModel):
    _inherit = 'ir.qweb'

    @QwebTracker.wrap_render
    @api.model
    def _render(self, template, values=None, **options):
        cfdi_data = super()._render(template, values=values, **options)
        if cfdi_data and (cfdi_data.find('xmlns__') or '') >= 0:
            cfdi_data = cfdi_data.replace('xmlns__', 'xmlns:')
            tree = fromstring(cfdi_data)
            schemaLocation = tree.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']
            schemaLocation = schemaLocation + " http://www.sat.gob.mx/detallista http://www.sat.gob.mx/sitio_internet/cfd/detallista/detallista.xsd"
            print("--------- schemaLocation", schemaLocation)            
            tree.attrib.update({
                "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": schemaLocation
            })
            print("---tree.attrib", tree.attrib)
            cfdi_data = etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8')
            cfdi_data = b' '.join(cfdi_data.split())
        return cfdi_data            


class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    detallista_purchase_reference = fields.Char('Número de pedido Comprador', required=False)
    detallista_purchase_reference_date = fields.Date('Fecha de pedido Comprador', default=lambda self: fields.Datetime.now(), required=False)
    additional_reference_identification = fields.Char('Número de referencia adicional', required=False)
    delivery_note_reference = fields.Char('Número de contra-recibo', required=False)
    delivery_note_date = fields.Date('Fecha de Recepción', default=lambda self: fields.Datetime.now(), required=False)
    person_or_department_name = fields.Char('Contacto de compras: No. o Nombre de departamento', required=False)
    alternate_party_identifaction = fields.Char('Número de emisor(proveedor)', required=False, default='0000950000442')
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


    l10n_mx_edi_detallista = fields.Boolean(
        string="Complemento Detallista?",
        readonly=False, store=True,
        compute='_compute_l10n_mx_edi_detallista',
        help="If this field is active, the CFDI that generates this invoice will include the complement "
             "'Detallista'.")

    def _auto_init(self):
        """
        Create compute stored field l10n_mx_edi_detallista
        here to avoid MemoryError on large databases.
        """
        if not column_exists(self.env.cr, 'account_move', 'l10n_mx_edi_detallista'):
            create_column(self.env.cr, 'account_move', 'l10n_mx_edi_detallista', 'boolean')
            # _compute_l10n_mx_edi_detallista uses res_partner.l10n_mx_edi_detallista,
            # which is a new field in this module hence all values set to False.
            self.env.cr.execute("UPDATE account_move set l10n_mx_edi_detallista=FALSE;")
        return super()._auto_init()    


    @api.depends('partner_id')
    def _compute_l10n_mx_edi_detallista(self):
        for move in self:
            if move.move_type == 'out_invoice':
                move.l10n_mx_edi_detallista = move.partner_id.l10n_mx_edi_detallista
            else:
                move.l10n_mx_edi_detallista = False

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


    # -------------------------------------------------------------------------
    # CFDI
    # -------------------------------------------------------------------------
    def _l10n_mx_edi_add_invoice_cfdi_values(self, cfdi_values):
        # EXTENDS 'l10n_mx_edi'
        self.ensure_one()
        super()._l10n_mx_edi_add_invoice_cfdi_values(cfdi_values)
        if cfdi_values.get('errors'):
            return

        detallista_values = cfdi_values['mx_detallista'] = {}
        if self.l10n_mx_edi_detallista:

            lineItems = []
            indx = 1
            subtotal = 0.0
            for line in self.invoice_line_ids:
                subtotal = subtotal + (line.price_unit * line.quantity)

                unitOfMeasure = ""
                if line.product_id.uom_id.name == 'Unidades':
                    unitOfMeasure = "UNIDAD"
                elif line.product_id.uom_id.name == 'Servicios':
                    unitOfMeasure = "SERVICIO"
                else:
                    unitOfMeasure = line.product_id.uom_id.name or ""

                item_tmp = {
                    "current_line": indx,
                    "subtotal": subtotal,
                    "barcode": line.product_id.barcode,
                    "default_code": line.product_id.default_code,
                    "name": line.name,
                    "unitOfMeasure": unitOfMeasure,
                    "quantity": line.quantity,
                    "price_unit": line.price_unit,
                    "netPrice": line.price_subtotal / line.quantity,
                    "grossAmount": line.price_unit * line.quantity,
                    "netAmount": line.price_subtotal
                }
                indx += 1

            amount_to_text = self.amount_to_text(self.amount_total_signed)
            detallista_values.update({
                "move_type": self.move_type,
                "amount_to_text": amount_to_text,
                "detallista_purchase_reference": self.detallista_purchase_reference,
                "detallista_purchase_reference_date": self.detallista_purchase_reference_date,
                "additional_reference_identification_type": self.additional_reference_identification_type,
                "additional_reference_identification": self.additional_reference_identification,
                "delivery_note_reference": self.delivery_note_reference,
                "delivery_note_date": self.delivery_note_date,
                "person_or_department_name": self.person_or_department_name,
                "alternate_party_identifaction": self.alternate_party_identifaction,
                "settlementType": self.settlementType,
                "special_services_type": self.special_services_type,
                "lineItems": lineItems,
                "subtotal": subtotal
            })
