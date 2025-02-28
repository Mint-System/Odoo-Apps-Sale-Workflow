import logging

_logger = logging.getLogger(__name__)
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _check_line_unlink(self):
        """Filter expense lines that can be deleted."""
        res = super()._check_line_unlink()
        return res.filtered(lambda line: not line.is_expense or line.qty_invoiced > 0)
