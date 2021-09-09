{
    'name': "Sale Order Line Position",

    'summary': """
        Use sale order line position for linked delivery orders and outgoing invoices.
    """,
    
    'author': 'Mint System GmbH, Odoo Community Association (OCA)',
    'website': 'https://www.mint-system.ch',
    'category': 'Sale',
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    
    'depends': ['sale_management'],

    'data': [
        'views/views.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}