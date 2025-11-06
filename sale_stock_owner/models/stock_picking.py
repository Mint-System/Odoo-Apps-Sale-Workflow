import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _set_or_remove_owner(self, location_id, action='set'):
        picking = self
        for line in picking.move_line_ids:
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
            if picking.picking_type_id.name == 'Returns': # better: code
                loc_id = picking.location_dest_id.id
                picking._set_or_remove_owner(loc_id, action='remove')
            elif (picking.owner_id and picking.location_id.clear_owner):
                loc_id = picking.location_id.id
                picking._set_or_remove_owner(location_id=loc_id, action='remove')
            elif picking.owner_id and not picking.location_id.clear_owner:
                loc_id = picking.location_id.id
                picking._set_or_remove_owner(location_id=loc_id, action='set')


        return res
