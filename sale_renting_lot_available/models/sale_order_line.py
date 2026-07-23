# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

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
        for line in self.filtered(lambda l: l.state == "sale"):
            line._create_stock_rental_lot()

    def _create_stock_rental_lot(self):
        """
        Create a stock.rental.slot entry for each slot or qty.
        """
        for line in self:
            line.rental_slot_ids.sudo().unlink()
            if line.is_rental and line.pickedup_lot_ids:
                for lot in line.pickedup_lot_ids:
                    line.env["stock.rental.slot"].create({"so_line_id": line.id, "lot_id": lot.id})
            elif line.is_rental and not line.rental_slot_ids:
                for _qty in range(int(line.product_uom_qty)):
                    self.env["stock.rental.slot"].create({"so_line_id": line.id})

    def unlink(self):
        self.rental_slot_ids.sudo().unlink()
        return super().unlink()
