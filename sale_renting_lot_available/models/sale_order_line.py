# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    rental_slot_ids = fields.One2many("stock.rental.slot", "so_line_id", string="Rental Slots")
    pickedup_lot_ids = fields.Many2many(
        "stock.lot",
        "rental_pickedup_lot_rel",
        domain="[('product_id', '=', product_id)]",
        copy=False,
        inverse="_inverse_pickedup_lot_ids",
    )

    def _inverse_pickedup_lot_ids(self):
        """
        Recreate stock.rental.slot entries when picked-up lots change.
        """
        for line in self:
            line._create_stock_rental_lot()

    def _create_stock_rental_lot(self):
        """
        Create a stock.rental.slot entry for rental lines.
        """
        for line in self:
            if line.is_rental and line.pickedup_lot_ids:
                self.env["stock.rental.slot"].search([("lot_id"), "in", line.pickedup_lot_ids]).unlink()
                line.rental_slot_ids.sudo().unlink()
                for lot in line.pickedup_lot_ids:
                    line.env["stock.rental.slot"].create({"so_line_id": line.id, "lot_id": lot.id})
            elif line.is_rental and not line.rental_slot_ids:
                self.env["stock.rental.slot"].create({"so_line_id": line.id})

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines._create_stock_rental_lot()
        return lines

    def unlink(self):
        _logger.warning(self.rental_slot_ids)
        self.rental_slot_ids.sudo().unlink()
        return super().unlink()
