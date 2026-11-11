# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrderLineWizard(models.TransientModel):
    _name = "rental.order.line.wizard"
    _description = "Rental Order Line Wizard"

    so_line_id = fields.Many2one("sale.order.line")
    product_uom_qty = fields.Float(readonly=True)

    def split(self):
        """
        Split a sale order line into one line per unit of quantity.

        The current line keeps the first unit and one new line is created for
        every additional unit. Reserved and picked up lots are distributed
        across the resulting lines, one lot per line.
        """
        self.ensure_one()
        so_line_id = self.so_line_id

        if so_line_id.rental_status in ["returned"]:
            raise UserError(
                _(
                    "Cannot split line with product '%s' in rental state 'returned'.",
                    so_line_id.product_id.name,
                )
            )

        qty = int(so_line_id.product_uom_qty)
        if qty <= 1:
            raise UserError(
                _(
                    "Cannot split line with product '%s'. Qty must be greater than 1.",
                    so_line_id.product_id.name,
                )
            )

        reserved_lot_ids = so_line_id.reserved_lot_ids
        pickedup_lot_ids = so_line_id.pickedup_lot_ids
        returned_lot_ids = so_line_id.returned_lot_ids
        qty_delivered = so_line_id.qty_delivered
        qty_returned = so_line_id.qty_returned

        # Keep one unit and the first lot on the current line. The delivered
        # and returned quantity must be reduced before the ordered quantity,
        # otherwise 'sale_stock' rejects the lower ordered qty as it is still
        # compared to the old delivered qty.
        # Both writes must be separate: 'sale_stock' compares the ordered qty
        # with the delivered qty stored in the database.
        so_line_id.write(
            {
                "qty_delivered": min(1.0, qty_delivered),
                "qty_returned": min(1.0, qty_returned),
            }
        )
        so_line_id.write(
            {
                "reserved_lot_ids": reserved_lot_ids[:1],
                "pickedup_lot_ids": pickedup_lot_ids[:1],
                "returned_lot_ids": returned_lot_ids[:1],
                "product_uom_qty": 1.0,
            }
        )

        # Create one new line for every additional unit
        new_lines = self.env["sale.order.line"]
        for index in range(qty - 1):
            lot_index = index + 1
            pickedup_lot = pickedup_lot_ids[lot_index : lot_index + 1]
            returned_lot = returned_lot_ids[lot_index : lot_index + 1]
            new_line = so_line_id.copy(
                default={
                    "order_id": so_line_id.order_id.id,
                    "product_uom_qty": 1.0,
                    "qty_delivered": min(1.0, max(0.0, qty_delivered - index)),
                    "qty_returned": min(1.0, max(0.0, qty_returned - index)),
                }
            )
            new_line.write(
                {
                    "reserved_lot_ids": reserved_lot_ids[lot_index : lot_index + 1],
                    "pickedup_lot_ids": pickedup_lot,
                    "returned_lot_ids": returned_lot,
                }
            )
            new_lines |= new_line

        return new_lines
