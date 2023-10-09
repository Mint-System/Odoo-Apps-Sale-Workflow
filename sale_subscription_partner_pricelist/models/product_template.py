import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    pricelist_id = fields.Many2one(comodel_name="product.pricelist", check_company=True)
