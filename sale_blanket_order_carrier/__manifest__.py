{
    "name": "Sale Blanket Order Carrier",
    "summary": """
        Set carrier on sale blanket order.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Uncategorized",
    "version": "14.0.1.1.0",
    "license": "AGPL-3",
    "depends": ["sale_blanket_order","delivery"],
    "data": ["views/view_blanket_order_form.xml", "views/view_order_form.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
