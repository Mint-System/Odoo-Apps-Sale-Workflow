from odoo import models




class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        new_picking_id, pick_type_id = super()._create_returns()

        new_picking = self.env['stock.picking'].browse(new_picking_id)

        new_picking.owner_id = False

        return new_picking_id, pick_type_id

