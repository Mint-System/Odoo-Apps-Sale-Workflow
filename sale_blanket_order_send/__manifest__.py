{
    "name": "Sale Blanket Order Send",
    "summary": """
        Send blanket order by e-mail.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Sale",
    "version": "14.0.1.1.1",
    "license": "AGPL-3",
    "depends": ["sale_blanket_order_date_confirmed"],
    "data": ["data/mail_data.xml", "views/sale_blanket_order.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
