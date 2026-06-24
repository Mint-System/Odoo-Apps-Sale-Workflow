# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Renting Lot Available",
    "summary": """
        Plan all rening product lots on gantt view.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "OPL-1",
    "depends": ["sale_renting_line_period"],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_lot_rental_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
}
