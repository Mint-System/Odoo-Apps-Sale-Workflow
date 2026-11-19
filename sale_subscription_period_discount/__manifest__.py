{
    "name": "Sale Subscription Period Discount",
    "summary": """
        Apply discounts on subscription periods.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Sales",
    "version": "18.0.1.0.0",
    "license": "OPL-1",
    "depends": ["sale_subscription"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_subscription_plan.xml",
        "views/sale_subscription.xml",
    ],
    "demo": ["demo/sale_subscription_plan_demo.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "qweb": ["static/src/xml/board.xml"],
}
