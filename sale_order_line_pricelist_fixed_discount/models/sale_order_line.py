import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "product_uom", "product_uom_qty")
    def _compute_price_unit(self):
        """Filter and apply pricelist rule with fixed discount."""
        super()._compute_price_unit()

        for line in self:

            # Read filter date from context
            date = (
                self._context.get("date")
                or line.order_id.commitment_date
                or line.order_id.date_order
            )

            # Apply fixed price discount
            line.discount = line.order_id.pricelist_id._get_fixed_discount(
                line.product_id, line.product_uom_qty, date
            )
