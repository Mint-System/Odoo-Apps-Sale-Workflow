# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = "stock.lot"

    rental_lot_ids = fields.One2many("stock.lot.rental", "lot_id", string="Rental Lots")

    def _create_stock_rental_lot(self):
        """Create a stock.lot.rental entry for rentable lots."""
        for lot in self:
            if lot.product_id.rent_ok:
                lot.env["stock.lot.rental"].create({"lot_id": lot.id})

    @api.model_create_multi
    def create(self, vals_list):
        lots = super().create(vals_list)
        lots._create_stock_rental_lot()
        return lots

    def write(self, vals):
        res = super().write(vals)
        if "active" in vals and not vals["active"]:
            rental_lots = self.env["stock.lot.rental"].search([("lot_id", "in", self.ids)])
            if rental_lots:
                rental_lots.write({"active": False})
        return res
