{
    'name': "Sale Order Delivery Note",

    'summary': """
        Add note that is printed on sale order and delivery slip report.
    """,
    
    'author': 'Mint System GmbH, Odoo Community Association (OCA)',
    'website': 'https://www.mint-system.ch',
    'category': 'Sale',
    'version': '14.0.1.1.0',
    'license': 'AGPL-3',
    
    'depends': ['sale_management', 'stock_delivery_note'],

    'data': [
        'views/sale_order_view.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}