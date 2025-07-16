{
    "name": "Sale Blanket Order Readonly States",
    "summary": """
        Override readonly states.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Sales",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale_blanket_order_cancel_state",
    ],
    "data": ["views/view_blanket_order_form.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
