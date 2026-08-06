# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Timesheet Billable",
    "summary": """
        Selection filter for order lines with billable products on timesheet entries and define if task is billable or not..
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["project", "sale_timesheet"],
    "data": [
        "views/account_analytic_line_views.xml",
        "views/project_view_task_form2_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
