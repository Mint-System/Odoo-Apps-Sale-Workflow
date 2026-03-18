import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    public_category_ids = fields.Many2many("product.public.category", string="Website categories")