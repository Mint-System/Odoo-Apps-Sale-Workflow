# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Timesheet Report Group Invoice Type",
    "summary": """
        Group timehsheet entries by invoice type on timesheet report.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_timesheet"],
    "data": [
        "report/hr_timesheet_templates.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
