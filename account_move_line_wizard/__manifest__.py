# __manifest__.py

{
    'name': 'Account Move Line Wizard',
    'version': '18.0.0.0',
    'license': 'LGPL-3',
    'category': 'Accounting',
    'summary': 'Wizard to change account in account move line',
    'author': 'Yeidala',
    'website': 'https://www.yeidala.com',
    'depends': ['account'],
    'data': [
        'views/change_account_wizard_view.xml',
        'views/account_move_line_action.xml',
    ],
    'installable': True,
    'application': False,
}
