{
    'name': 'Complemento Detallista',
    'version': '16.0.1.0',
    'summary': '',
    'author': 'Yeidala',
    'website': 'www.yeidala.com',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'base', 
        'account', 
        'l10n_mx_edi', 
        'l10n_mx_edi_40',
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

