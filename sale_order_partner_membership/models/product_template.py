import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    membership_ok = fields.Boolean(
        "Is Membership",
        default=False,
        help="Product is a membership.",
    )
