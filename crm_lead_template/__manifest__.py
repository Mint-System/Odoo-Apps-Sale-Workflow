# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "CRM Lead Template",
    "summary": """
        Create lead notes from template..
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["crm"],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead_views.xml",
        "views/crm_lead_template_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
