# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class RentalOrderWizardLine(models.TransientModel):
    _inherit = "rental.order.wizard.line"

    @api.model
    def _default_wizard_line_vals(self, line, status):
        """
        Override pickeable lots to use stock.rental.slot availability.
        """
        res = super()._default_wizard_line_vals(line, status)

        if status == "pickup" and line.product_id.tracking == "serial":
            # Find lots that are unavailable because another line has booked them
            # in an overlapping time range.
            overlapping_booked = self.env["stock.rental.slot"].search(
                [
                    ("is_placeholder", "=", False),
                    ("so_line_id", "!=", line.id),
                    ("product_id", "=", line.product_id.id),
                    ("start_date", "<=", line.rental_return_date),
                    ("return_date", ">=", line.rental_start_date),
                ]
            )
            unavailable_lots = overlapping_booked.mapped("lot_id")

            # All lots that have any slot record (placeholder or booked) for this product
            all_slots = self.env["stock.rental.slot"].search(
                [("product_id", "=", line.product_id.id), ("lot_id", "!=", False)]
            )
            pickeable_lots = all_slots.mapped("lot_id") - unavailable_lots

            # Exclude lots already picked up or returned on this line
            # (same guard as the original stock-based implementation)
            pickeable_lots -= line.pickedup_lot_ids
            pickeable_lots -= line.returned_lot_ids

            reserved_lots = line.reserved_lot_ids & pickeable_lots

            res.update(
                {
                    "qty_delivered": len(reserved_lots),
                    "pickedup_lot_ids": [(6, 0, reserved_lots.ids)],
                    "pickeable_lot_ids": [(6, 0, pickeable_lots.ids)],
                }
            )

        return res
