{
    "name": "Sale Blanket Order Readonly States",
    "summary": """
        Override readonly states.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Sales",
    "version": "14.0.1.1.0",
    "license": "AGPL-3",
    "depends": [
        "sale_blanket_order_invoice_shipping_partner",
        "sale_blanket_order_cancel_state",
        "sale_blanket_order_contact_person",
        "sale_blanket_order_stock_terms",
    ],
    "data": ["views/view_blanket_order_form.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}