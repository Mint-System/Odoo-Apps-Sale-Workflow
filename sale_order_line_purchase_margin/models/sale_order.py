from odoo import api, models
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('procurement_group_id.stock_move_ids.created_purchase_line_id.order_id', 'procurement_group_id.stock_move_ids.move_orig_ids.purchase_line_id.order_id')
    def _compute_purchase_order_count(self):
        """Link order lines with purchase order lines."""
        super(SaleOrder, self)._compute_purchase_order_count()
        
        purchase_ids = self._get_purchase_orders()
        for line in self.order_line:
            purchase_line_ids = purchase_ids.order_line.filtered(lambda l: l.product_id == line.product_id)
            line.write({'purchase_line_ids': purchase_line_ids.ids })
