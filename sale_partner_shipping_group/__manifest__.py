{
    "name": "Sale Partner Shipping Group",
    "summary": """
        Access group for shipping address on sale orders and invoices.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Technical",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale", "account"],
    "data": ["security/security.xml", "views/account_move.xml", "views/sale_order.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
