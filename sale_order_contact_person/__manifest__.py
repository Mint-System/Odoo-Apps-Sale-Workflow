{
    "name": "Sale Order Contact Person",
    "summary": """
        Set contact person on sale order.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Sale",
    "version": "14.0.2.1.0",
    "license": "AGPL-3",
    "depends": ["sale", "partner_type_sale", "account_invoice_sale_partner"],
    "data": ["views/sale_order_view.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
