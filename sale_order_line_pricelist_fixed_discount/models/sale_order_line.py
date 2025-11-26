import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _compute_discount(self):
        """
        Filter and apply pricelist rule with fixed discount.
        """
        res = super()._compute_discount()
        for line in self:
            # Read filter date from context
            date = self._context.get("date") or line.order_id.commitment_date or line.order_id.date_order

            # Apply fixed price discount
            line.discount = line.order_id.pricelist_id._get_percent_price(line.product_id, line.product_uom_qty, date)
        return res
