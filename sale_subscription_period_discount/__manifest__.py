{
    "name": "Sale Subscription Period Discount",
    "summary": """
        Apply discounts on subscription periods.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Sales",
    "version": "16.0.1.1.0",
    "license": "OPL-1",
    "depends": ["sale_subscription"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_temporal_recurrence.xml",
        "views/sale_subscription.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "qweb": ["static/src/xml/board.xml"],
}
