# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrderLineWizard(models.TransientModel):
    _name = "rental.order.line.wizard"
    _description = "Rental Order Line Wizard"

    so_line_id = fields.Many2one("sale.order.line")
    qty_diff = fields.Float()
    product_uom_qty = fields.Float(readonly=True)

    def split(self, transfer_lot_ids=None):
        """
        Duplicate sale order line.
        The qty diff is subtracted on current line and set on new line.
        """
        self.ensure_one()
        so_line_id = self.so_line_id

        if so_line_id.rental_status in ["returned"]:
            raise UserError(
                _(
                    "Cannot split line with product '%s' in retnal state 'returned'.",
                    so_line_id.product_id.name,
                )
            )

        if self.qty_diff <= 0 or self.qty_diff >= self.product_uom_qty:
            raise UserError(
                _(
                    "Cannot split line with product '%s'. Qty diff must be strictly between 0 and %s.",
                    so_line_id.product_id.name,
                    self.product_uom_qty,
                )
            )

        # Adjust qty on current line
        if so_line_id.qty_delivered > 0:
            so_line_id.qty_delivered -= self.qty_diff
        so_line_id.product_uom_qty -= self.qty_diff

        new_line = so_line_id.copy(
            default={
                "order_id": so_line_id.order_id.id,
                "product_uom_qty": self.qty_diff,
                "qty_delivered": self.qty_diff,
            }
        )

        # Transfer lot to new line
        if so_line_id.reserved_lot_ids and so_line_id.pickedup_lot_ids:
            # Select the amount of lots based on qty diff
            reserved_lot_ids = so_line_id.reserved_lot_ids
            pickedup_lot_ids = so_line_id.pickedup_lot_ids

            # _logger.warning([self.qty_diff, reserved_lot_ids])
            transfer_reserved_lot_ids = reserved_lot_ids[: int(self.qty_diff)]
            transfer_pickedup_lot_ids = pickedup_lot_ids[: int(self.qty_diff)]

            # Remove the lots from current line
            so_line_id.write(
                {
                    "reserved_lot_ids": reserved_lot_ids - transfer_reserved_lot_ids,
                    "pickedup_lot_ids": pickedup_lot_ids - transfer_pickedup_lot_ids,
                }
            )

            # Add lots to new line
            new_line.write(
                {
                    "reserved_lot_ids": transfer_reserved_lot_ids,
                    "pickedup_lot_ids": transfer_pickedup_lot_ids,
                }
            )

        return new_line
