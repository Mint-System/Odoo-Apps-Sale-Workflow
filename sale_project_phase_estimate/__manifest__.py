# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Project Phase Estimate",
    "summary": """
        Link sale order lines with project phase estimates.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_project", "project_phase_estimate"],
    "data": [
        "views/project_estimate_views.xml",
        "views/sale_order_views.xml",
        "views/project_project_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
