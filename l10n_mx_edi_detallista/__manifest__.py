{
    'name': 'Complemento Detallista',
    'version': '18.0.1.2.0',
    'summary': 'Este módulo permite agregar el complemento detallista a un comprobante, antes del firmado local del mismo.',
    'author': 'Yeidala',
    'website': 'www.yeidala.com',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'base_setup', 
        'account', 
        'l10n_mx_edi'
    ],
    'data': [
        'data/cfdi_detallista.xml',
        'views/res_partner_views.xml',
        'views/account_move_view.xml'
    ],
    'demo': [],
    'auto_install': False,
    'application': False,
    'assets': {
    }
}

