import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

from .config import DURATION_SELECTION


class ProductTemplate(models.Model):
    _inherit = "product.template"

    duration = fields.Selection(selection=DURATION_SELECTION)
