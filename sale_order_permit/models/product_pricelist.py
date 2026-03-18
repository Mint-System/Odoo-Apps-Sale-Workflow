import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    is_dummy = fields.Boolean(help="Used as a placeholder. Products are hidden until another pricelist is selected.")

    public_category_ids = fields.Many2many("product.public.category", string="Website categories")