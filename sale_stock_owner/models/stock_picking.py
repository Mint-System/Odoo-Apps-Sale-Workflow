import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _action_done(self):
        res = super()._action_done()
        for picking in self:
            _logger.warning(f"########## picking owner: {picking.owner_id}, picking type: {picking.picking_type_id}, {picking.picking_type_id.name}, {picking.picking_type_code}")
            # alternative 1: add owner to stock
            if (picking.owner_id and picking.location_id.clear_owner) or picking.picking_type_id.name == 'Returns':
                _logger.warning("###### remove owner")
                picking.write({"owner_id": False})
                for line in picking.move_line_ids:
                    _logger.warning(f"########## product: {line.product_id.name}, lot: {line.lot_id.name}, loc: {picking.location_id.name}, dest loc {picking.location_dest_id.name}")
                    loc_id = picking.location_dest_id.id if picking.picking_type_id.name == 'Returns' else picking.location_id.id
                    stock_quants = self.env["stock.quant"].search(
                        [
                            ("product_id", "=", line.product_id.id),
                            ("lot_id", "=", line.lot_id.id),
                            ("location_id", "=", loc_id),
                        ]
                    )
                    _logger.warning(f"stock quants: {stock_quants}")
                    stock_quants.write({"owner_id": False})

            if picking.owner_id and not picking.location_id.clear_owner:
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
