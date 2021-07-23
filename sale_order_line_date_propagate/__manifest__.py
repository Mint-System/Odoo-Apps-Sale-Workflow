{
    'name': "Sale Order Line Date Propagate",

    'summary': """
        This module ensure that line order date are propagated to stock pickings.
    """,
    
    'author': 'Mint System GmbH, Odoo Community Association (OCA)',
    'website': 'https://www.mint-system.ch',
    'category': 'Manufacturing',
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    
    'depends': ['sale_order_line_date'],

    'installable': True,
    'application': False,
}