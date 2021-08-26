{
    'name': "Sale Blanket Order Notes",

    'summary': """
        Notes for sale blanket and sale orders.
    """,
    
    'author': 'Mint System GmbH, Odoo Community Association (OCA)',
    'website': 'https://www.mint-system.ch',
    'category': 'Sale',
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    
    'depends': ['sale_blanket_order'],

    'data': [
        'views/sale_order.xml',
        'views/sale_blanket_order.xml'
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}