# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class RentalOrderWizardLine(models.TransientModel):
    _inherit = "rental.order.wizard.line"

    return_date = fields.Datetime(required=True)

    @api.model
    def _default_wizard_line_vals(self, line, status):
        """
        Set default return date.
        Remove lots that have been removed on sibling lines.
        """
        res = super()._default_wizard_line_vals(line, status)
        _logger.warning([line, status])
        if status == "return":
            now = fields.Datetime.now()
            res["return_date"] = now if line.start_date < now else line.return_date
        else:
            res["return_date"] = line.return_date

        if res["returnable_lot_ids"]:
            # Check if lots have been returned on other lines of the same order and product
            other_returned_lots = line.same_product_line_ids.mapped("returned_lot_ids")

            # Remove the already returned lots from returnable
            if other_returned_lots:
                returnable_ids = res["returnable_lot_ids"][0][2]
                returnable_ids = [lot_id for lot_id in returnable_ids if lot_id not in other_returned_lots.ids]
                res["returned_lot_ids"] = [(6, 0, returnable_ids)]

        return res

    def _apply(self):
        """
        Update line return date and split order lines if partial qty is returned.
        """
        res = super()._apply()
        for wizard_line in self:
            order_line = wizard_line.order_line_id
            if order_line.rental_start_date > wizard_line.return_date:
                raise UserError(
                    _(
                        "Return date cannot be before start date. Check line with product '%s'.",
                        order_line.product_id.name,
                    )
                )

            # Partial return
            if wizard_line.qty_returned > 0 and wizard_line.qty_returned < wizard_line.qty_delivered:
                # Get remaining qty
                qty_returned = wizard_line.qty_returned
                qty_remaining = wizard_line.qty_delivered - qty_returned

                # Get reaminign lots
                pickedup_lot_ids = order_line.pickedup_lot_ids
                returned_lot_ids = wizard_line.returned_lot_ids
                remaining_lot_ids = pickedup_lot_ids - returned_lot_ids

                # Current line has remining quanity
                order_line.write({"qty_delivered": qty_remaining})
                order_line.write({"product_uom_qty": qty_remaining, "qty_returned": 0.0, "returned_lot_ids": False})

                # Create new line with returned quanity.
                returned_line = order_line.copy()
                returned_line.write(
                    {
                        "product_uom_qty": qty_returned,
                        "qty_delivered": qty_returned,
                        "qty_returned": qty_returned,
                        "rental_return_date": wizard_line.return_date,
                    }
                )

                # Update lot ids
                if remaining_lot_ids:
                    returned_line.write(
                        {
                            "pickedup_lot_ids": returned_lot_ids,
                            "returned_lot_ids": returned_lot_ids,
                        }
                    )

            # Full return
            elif wizard_line.qty_returned > 0 and wizard_line.qty_returned == wizard_line.qty_delivered:
                order_line.write({"rental_return_date": wizard_line.return_date})

        return res
