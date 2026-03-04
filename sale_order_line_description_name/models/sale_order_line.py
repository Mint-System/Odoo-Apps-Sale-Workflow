import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _compute_name(self):
        res = super()._compute_name()
        for line in self:
            if line.product_id and line.name:
                if line.product_id.display_name and line.product_id.name:
                    line.name = line.name.replace(line.product_id.display_name, line.product_id.name)
            elif line.product_id and not line.name:
                line.name = line.product_id.name
            else:
                line.name = ""
