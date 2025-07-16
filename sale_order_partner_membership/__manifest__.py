{
    "name": "Sale Order Partner Membership",
    "summary": """
        Set membership address on sale order.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Sales",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale", "partner_type_membership"],
    "data": ["views/sale_order.xml", "views/product_template.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
