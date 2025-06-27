import logging

_logger = logging.getLogger(__name__)
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    release_id = fields.Many2one("helm.release")
