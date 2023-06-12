{
    "name": "Sale Expense Unlink",
    "summary": """
        Allow deletion of sale order expense lines.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Sales",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_expense_link"],
    "data": ["views/hr_expense_sheet.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "qweb": ["static/src/xml/board.xml"],
}
