# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Permit",
    "summary": """
        Adds Workflow for selling permits.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch",
    "category": "Repository",
    "development_status": "Production/Stable",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "base_partner_sequence",
        "partner_contact_birthdate",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "views/product_pricelist_views.xml",
        "views/res_partner_views.xml",
        "views/permit_sequence.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
