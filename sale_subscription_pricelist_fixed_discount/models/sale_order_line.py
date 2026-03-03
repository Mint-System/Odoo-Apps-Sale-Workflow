import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _compute_discount(self):
        """
        The _compute_discount method in sale_subscription/models/sale_order_line.py removes
        lines from super calls. This method is a copy of sale_order_line_pricelist_fixed_discount.
        """
        super()._compute_discount()

        for line in self:
            # Read filter date from context
            date = self._context.get("date") or line.order_id.commitment_date or line.order_id.date_order

            # Apply fixed price discount
            discount = line.order_id.pricelist_id._get_percent_price(line.product_id, line.product_uom_qty, date)
            line.discount = discount
