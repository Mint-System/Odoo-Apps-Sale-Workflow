import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()
        for picking in self:
            if picking.owner_id:
                for line in picking.move_line_ids:
                    stock_quants = self.env["stock.quant"].search(
                        [
                            ("product_id", "=", line.product_id.id),
                            ("lot_id", "=", line.lot_id.id),
                            ("location_id", "=", picking.location_id.id),
                        ]
                    )
                    _logger.warning(["Set owner_id for:", stock_quants])
                    # stock_quants.write({"owner_id": picking.owner_id.id})
        return res


    def _action_done(self):
        res = super()._action_done()
        for picking in self:
            if picking.owner_id:
                for line in picking.move_line_ids:
                    stock_quants = self.env["stock.quant"].search(
                        [
                            ("product_id", "=", line.product_id.id),
                            ("lot_id", "=", line.lot_id.id),
                            ("location_id", "=", picking.location_id.id),
                        ]
                    )
                    stock_quants.write({"owner_id": picking.owner_id.id})
        
        return res