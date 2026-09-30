# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Project Report",
    "summary": """
        Adds project report for sold and recorded hours analysis.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Project",
    "development_status": "Production/Stable",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_timesheet"],
    "data": [
        "security/sale_project_report_security.xml",
        "security/ir.model.access.csv",
        "views/project_report_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
