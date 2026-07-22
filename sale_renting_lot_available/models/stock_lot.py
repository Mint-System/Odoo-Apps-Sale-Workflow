# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = "stock.lot"

    rental_slot_ids = fields.One2many("stock.rental.slot", "lot_id", string="Rental Slots")

    def _create_stock_rental_lot(self):
        """Create a stock.rental.slot entry for rentable lots."""
        for lot in self:
            if lot.product_id.rent_ok:
                lot.env["stock.rental.slot"].create({"lot_id": lot.id})

    @api.model_create_multi
    def create(self, vals_list):
        lots = super().create(vals_list)
        lots._create_stock_rental_lot()
        return lots

    def unlink(self):
        self.rental_slot_ids.sudo().unlink()
        return super().unlink()
