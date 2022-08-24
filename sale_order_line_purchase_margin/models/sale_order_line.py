from odoo import api, models
import logging
_logger = logging.getLogger(__name__)
from statistics import mean


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom', 'purchase_line_ids')
    def _compute_purchase_price(self):
        """Get average price from linked purchase order lines."""
        super()._compute_purchase_price()
        for line in self.filtered('purchase_line_ids'):
            line.purchase_price = mean(line.purchase_line_ids.mapped('price_unit'))
