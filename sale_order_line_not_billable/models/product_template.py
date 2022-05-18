import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    billable = fields.Boolean(default=True)