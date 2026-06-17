# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Renting Line Period",
    "summary": """
        Set rental start and end date on order line.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "OPL-1",
    "depends": ["sale_stock_renting"],
    "data": [
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
        "wizard/rental_order_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
