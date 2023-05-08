{
    "name": "Sale Expense Link",
    "summary": """
        Link expense ande sale order line.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Sales",
    "version": "15.0.1.1.0",
    "license": "AGPL-3",
    "depends": ["sale_expense"],
    "data": ["views/hr_expense_sheet.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "qweb": ["static/src/xml/board.xml"],
}