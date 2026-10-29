# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _generate_stock_rental_lot(self):
        for quant in self.filtered(lambda q: q.lot_id and q.lot_id.product_id.rent_ok):
            lot = quant.lot_id
            if lot.product_qty <= 0.0 and lot.start_slot_id:
                lot.start_slot_id.unlink()
            elif lot.product_qty > 0.0 and not lot.start_slot_id:
                lot._create_stock_rental_lot()

    @api.model_create_multi
    def create(self, vals_list):
        quants = super().create(vals_list)
        quants._generate_stock_rental_lot()
        return quants

    def write(self, vals):
        res = super().write(vals)
        if "quantity" in vals or "inventory_quantity" in vals or "inventory_quantity_auto_apply" in vals:
            self._generate_stock_rental_lot()
        return res

    def unlink(self):
        lots = self.mapped("lot_id")
        res = super().unlink()
        for lot in lots.filtered(lambda l: l.product_id.rent_ok):
            if lot.product_qty <= 0.0 and lot.start_slot_id:
                lot.start_slot_id.unlink()
            elif lot.product_qty > 0.0 and not lot.start_slot_id:
                lot._create_stock_rental_lot()
        return res
