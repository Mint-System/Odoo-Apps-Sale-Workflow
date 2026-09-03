import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _process_auto_invoice(self, invoice):
        """OVERWRITE: Do not post invoice"""
        return
