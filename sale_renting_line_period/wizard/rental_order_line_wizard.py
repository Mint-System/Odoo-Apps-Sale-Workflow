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

        # Keep one unit and the first lot on the current line. Reduce the
        # delivered quantity before the ordered quantity so that the
        # 'sale_stock' check does not reject the lower ordered qty.
        so_line_id.write(
            {
                "qty_delivered": 1.0 if pickedup_lot_ids else 0.0,
                "reserved_lot_ids": reserved_lot_ids[:1],
                "pickedup_lot_ids": pickedup_lot_ids[:1],
            }
        )
        so_line_id.write({"product_uom_qty": 1.0})

        # Create one new line for every additional unit
        new_lines = self.env["sale.order.line"]
        for index in range(qty - 1):
            lot_index = index + 1
            pickedup_lot = pickedup_lot_ids[lot_index : lot_index + 1]
            new_line = so_line_id.copy(
                default={
                    "order_id": so_line_id.order_id.id,
                    "product_uom_qty": 1.0,
                    "qty_delivered": 1.0 if pickedup_lot else 0.0,
                }
            )
            new_line.write(
                {
                    "reserved_lot_ids": reserved_lot_ids[lot_index : lot_index + 1],
                    "pickedup_lot_ids": pickedup_lot,
                }
            )
            new_lines |= new_line

        return new_lines
