{
    "name": "Sale Order Partner Pricelist",
    "summary": """
        Grant pricelist access with sale order.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Sales",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale"],
    "data": ["views/product_template.xml", "views/res_partner.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "qweb": ["static/src/xml/board.xml"],
}
