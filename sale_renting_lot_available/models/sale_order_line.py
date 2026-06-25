# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    rental_lot_ids = fields.One2many("stock.lot.rental", "so_line_id", string="Rental Lots")

    pickedup_lot_ids = fields.Many2many(
        "stock.lot",
        "rental_pickedup_lot_rel",
        domain="[('product_id', '=', product_id)]",
        copy=False,
        inverse="_inverse_pickedup_lot_ids",
    )

    def _inverse_pickedup_lot_ids(self):
        """Create or update stock.lot.rental entries when picked-up lots change."""
        for line in self:
            existing = line.rental_lot_ids
            if existing:
                existing.unlink()
            if line.is_rental and line.pickedup_lot_ids:
                for lot in line.pickedup_lot_ids:
                    line.env["stock.lot.rental"].create(
                        {"so_line_id": line.id, "lot_id": lot.id}
                    )

    def _create_stock_rental_lot(self):
        """
        Create a stock.lot.rental entry per picked-up lot for rental lines.
        """
        for line in self:
            if line.is_rental and line.pickedup_lot_ids:
                for lot in line.pickedup_lot_ids:
                    line.env["stock.lot.rental"].create({"so_line_id": line.id, "lot_id": lot.id})

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines._create_stock_rental_lot()
        return lines

    def unlink(self):
        self.rental_lot_ids.unlink()
        return super().unlink()
