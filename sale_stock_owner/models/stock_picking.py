import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _set_or_remove_owner(self, location_id, action='set'):
        picking = self
        for line in picking.move_line_ids:
            _logger.warning(f"########## product: {line.product_id.name}, lot: {line.lot_id.name}, loc: {picking.location_id.name}, dest loc {picking.location_dest_id.name}")
            loc_id = picking.location_dest_id.id if picking.picking_type_id.name == 'Returns' else picking.location_id.id
            stock_quants = self.env["stock.quant"].search(
                [
                    ("product_id", "=", line.product_id.id),
                    ("lot_id", "=", line.lot_id.id),
                    ("location_id", "=", location_id),
                ]
            )
            _logger.warning(f"stock quants: {stock_quants}")
            if action == 'remove':
                stock_quants.write({"owner_id": False})
            elif action == 'set':
                stock_quants.write({"owner_id": picking.owner_id.id})


    def _action_done(self):
        res = super()._action_done()
        for picking in self:
            _logger.warning(f"########## picking owner: {picking.owner_id}, picking type: {picking.picking_type_id}, {picking.picking_type_id.name}, {picking.picking_type_code}")
            
            if picking.picking_type_id.name == 'Returns':
                loc_id = picking.location_dest_id.id if picking.picking_type_id.name == 'Returns'
                picking._set_or_remove_owner(loc_id)
            elif (picking.owner_id and picking.location_id.clear_owner):
                picking.write({"owner_id": False})
                loc_id = picking.location_id.id
                picking._set_or_remove_owner(locvation_id=loc_id, action='remove')
            elif picking.owner_id and not picking.location_id.clear_owner:
                loc_id = picking.location_id.id
                picking._set_or_remove_owner(location_id=loc_id, action='set')

        return res
