from odoo import models, api


import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_uom_qty')
    def _onchange_product_id_set_product_packaging(self):
        if self.product_id.packaging_ids:
            packaging_ids = self.product_id.packaging_ids
            # .filtered(
            #     lambda p: (p.qty == 0.0) or (self.product_uom_qty <= p.qty > 0.0)
            # )
            _logger.warning(packaging_ids)
            self.product_packaging = packaging_ids[0] if packaging_ids else False
        