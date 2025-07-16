{
    "name": "Sale Blanket Order Readonly States Extended",
    "summary": """
        Sets readonly states for other sale blanket order modules.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Sales",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale_blanket_order_readonly_states",
        "sale_blanket_order_invoice_shipping_partner",
        "sale_blanket_order_contact_person",
        "sale_blanket_order_stock_terms",
    ],
    "data": ["views/view_blanket_order_form.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
