from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order'

    def action_cancel(self):
        """Cancel manufacturing orders in procurement group."""
        self.ensure_one()
        procurement_groups = self.env['procurement.group'].search([('sale_id', 'in', self.ids)])
        mrp_production_ids = procurement_groups.stock_move_ids.created_production_id.procurement_group_id.mrp_production_ids |\
            procurement_groups.mrp_production_ids
        
        _logger.warning(mrp_production_ids)
        mrp_production_ids.action_cancel()

        return super().action_cancel()