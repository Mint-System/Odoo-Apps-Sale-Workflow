# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

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
    product_uom_qty = fields.Float(
        inverse="_inverse_product_uom_qty",
    )
    available_slot_ids_count = fields.Integer(compute="_compute_available_slot_ids_count")

    def _inverse_product_uom_qty(self):
        """
        Generate slot when qty changes.
        """
        for line in self.filtered(lambda l: l.state != "cancel"):
            if line.is_rental and line.product_uom_qty > line.available_slot_ids_count:
                raise UserError(
                    _(
                        "The currently available rental qty for '%s' is %s.",
                        line.product_id.name,
                        line.available_slot_ids_count,
                    )
                )
            if line.state != "cancel":
                line._generate_stock_rental_lot()

    def _inverse_pickedup_lot_ids(self):
        """
        Generate slot entries when picked-up lots change.
        """
        for line in self.filtered(lambda l: l.state == "sale"):
            line._generate_stock_rental_lot()

    def _generate_stock_rental_lot(self):
        """
        Unlink existing and create new stock.rental.slot entry for each lot or qty.
        """
        for line in self:
            line.rental_slot_ids.sudo().unlink()

            # Create pickedup slots
            if line.is_rental and line.pickedup_lot_ids and not line.returned_lot_ids:
                for lot in line.pickedup_lot_ids:
                    line.env["stock.rental.slot"].create({"so_line_id": line.id, "lot_id": lot.id})

            # Update slot if returned
            elif line.is_rental and line.returned_lot_ids:
                pickedup_slot_ids = line.order_id.order_line.rental_slot_ids
                for lot in line.pickedup_lot_ids:
                    pickedup_slot_id = pickedup_slot_ids.filtered(lambda p: p.lot_id == lot)
                    if pickedup_slot_id:
                        pickedup_slot_id.write({"so_line_id": line.id})

            # Create qty slots
            elif line.is_rental and not line.rental_slot_ids:
                for _qty in range(int(line.product_uom_qty)):
                    self.env["stock.rental.slot"].create({"so_line_id": line.id})

    def unlink(self):
        self.rental_slot_ids.sudo().unlink()
        return super().unlink()

    def _compute_available_slot_ids_count(self):
        """
        For rental products with lots count placeholder slots minus the booked slots in time range.
        For stored rental products without lot return stored qty as count.
        """
        for line in self:
            if line.product_id.tracking in ["serial", "lot"]:
                # Get all placeholder slots of a product
                product_placeholder_slot_count = self.env["stock.rental.slot"].search_count(
                    [("is_placeholder", "=", True), ("product_id", "=", line.product_id)]
                )

                # Get all booked slots
                product_booked_slot_count = self.env["stock.rental.slot"].search_count(
                    [
                        ("is_placeholder", "=", False),
                        ("so_line_id", "!=", line.id),
                        ("product_id", "=", line.product_id.id),
                        ("start_date", "<=", line.return_date),
                        ("return_date", ">=", line.start_date),
                    ]
                )

                line.available_slot_ids_count = product_placeholder_slot_count - product_booked_slot_count

            elif line.product_id.is_storable and line.product_id.tracking == "none":
                line.available_slot_ids_count = line.product_id.qty_available
            else:
                line.available_slot_ids_count = 9999
