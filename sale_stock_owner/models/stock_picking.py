import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            if picking.owner_id:
                stock_quants = self.env["stock.quant"].search(
                    [
                        ("product_id", "=", picking.product_id.id),
                        ("location_id", "=", picking.location_id.id),
                    ]
                )
                stock_quant = stock_quants[0]
                stock_quant.write({"owner_id": picking.owner_id.id})
        res = super().button_validate()
        return res
