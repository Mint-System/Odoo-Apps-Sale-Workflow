{
    "name": "Sale Expense Link",
    "summary": """
        Link expense and sale order line.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Sales",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_expense"],
    "data": ["views/hr_expense_sheet.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "qweb": ["static/src/xml/board.xml"],
}
