{
    "name": "Sale Order Project Key",
    "summary": """
        Use number of linked project as sale order name.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Sales",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_timesheet", "project_key_link_type"],
    "data": ["views/sale_order.xml", "views/project_project.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
