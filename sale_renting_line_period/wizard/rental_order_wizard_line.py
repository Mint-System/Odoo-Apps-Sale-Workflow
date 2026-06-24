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
        Support setting a return date.
        Remove lots that have been removed on sibling lines.
        """
        res = super()._default_wizard_line_vals(line, status)
        res["return_date"] = line.return_date

        if res["returnable_lot_ids"]:
            # Check if lots have been returned on other lines of the same order and product
            other_returned_lots = line.order_id.order_line.filtered(
                lambda l: l.id != line.id and l.product_id.id == line.product_id.id and l.returned_lot_ids
            ).returned_lot_ids

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
            if wizard_line.qty_returned > 0 and wizard_line.qty_returned < wizard_line.qty_delivered:
                if order_line.rental_start_date > wizard_line.return_date:
                    raise UserError(
                        _(
                            "Return date cannot be before start date. Check line with product '%s'.",
                            order_line.product_id.name,
                        )
                    )

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
                    # Bug: The commented causes this issue
                    # File "enterprise/sale_stock_renting/models/sale_order_line.py", line 318, in _return_serials
                    # if ml.lot_id.id in lot_ids:
                    # order_line.write(
                    #     {
                    #         "returned_lot_ids": returned_lot_ids,
                    #     }
                    # )
                    returned_line.write(
                        {
                            "pickedup_lot_ids": returned_lot_ids,
                            "returned_lot_ids": returned_lot_ids,
                        }
                    )
        return res
