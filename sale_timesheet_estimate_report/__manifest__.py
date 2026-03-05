# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Timesheet Estimate Report",
    "summary": """
        Shows the projects estimates on the timesheet report.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "16.0.1.0.0",
    "license": "AGPL-3,OPL-1",
    "depends": ["sale_timesheet", "project_phase_estimate"],
    "data": [
        "report/hr_timesheet_templates.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
