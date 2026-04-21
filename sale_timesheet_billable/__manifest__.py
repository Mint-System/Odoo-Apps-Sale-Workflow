# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Timesheet Billable",
    "summary": """
        Selection filter for order lines with billable products on timesheet entries.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_timesheet", "project_task_billable"],
    "data": [
        "views/account_analytic_line_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
