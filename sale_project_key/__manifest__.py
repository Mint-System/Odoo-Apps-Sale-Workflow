# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Project Key",
    "summary": """
        Show project key on sale order.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_project", "project_key"],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
