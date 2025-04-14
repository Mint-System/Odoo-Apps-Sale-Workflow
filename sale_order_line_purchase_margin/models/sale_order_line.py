import logging
from statistics import mean

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    stock_purchase_line_ids = fields.Many2many(
        "purchase.order.line", compute="_compute_stock_purchase_lines", store=False
    )

    def _compute_stock_purchase_lines(self):
        """Get average price from linked purchase order lines."""
        for line in self:
            stock_purchase_line_ids = []
            purchase_ids = line.order_id._get_purchase_orders()
            if purchase_ids:
                stock_purchase_line_ids = purchase_ids.order_line.filtered(
                    lambda l: l.product_id == line.product_id
                )
                if stock_purchase_line_ids:
                    line.purchase_price = mean(
                        stock_purchase_line_ids.mapped("price_unit")
                    )
            line.stock_purchase_line_ids = stock_purchase_line_ids
