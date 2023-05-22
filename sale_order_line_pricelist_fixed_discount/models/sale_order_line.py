from odoo import fields, models, _, api
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.onchange('product_id', 'price_unit', 'product_uom_qty')
    def _onchange_price_rule(self):
        """Filter and apply pricelist rule with fixed discount."""

        # Read filter date from context
        date = self._context.get('date') or self.order_id.commitment_date or self.order_id.date_order

        # Apply fixed price discount
        price_discount = self.order_id.pricelist_id._get_fixed_discount(self.product_id, self.product_uom_qty, date)
        if price_discount != 0.0:
            self.discount = price_discount
