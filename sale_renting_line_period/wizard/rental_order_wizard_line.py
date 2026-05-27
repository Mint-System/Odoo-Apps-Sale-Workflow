# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class RentalOrderWizardLine(models.TransientModel):
    _inherit = "rental.order.wizard.line"

    return_date = fields.Datetime(default=fields.Datetime.now, required=True)

    def _apply(self):
        """
        Update line return date and split order lines if partial qty is returned.
        """
        res = super()._apply()
        for wizard_line in self:
            order_line = wizard_line.order_line_id
            _logger.warning([wizard_line.qty_returned, wizard_line.qty_delivered])
            if wizard_line.qty_returned > 0 and wizard_line.qty_returned < wizard_line.qty_delivered:
                qty_returned = wizard_line.qty_returned
                qty_remaining = wizard_line.qty_delivered - qty_returned

                order_line.update(
                    {"product_uom_qty": qty_remaining, "qty_delivered": qty_remaining, "qty_returned": 0.0}
                )
                returned_line = order_line.copy()
                returned_line.update(
                    {
                        "product_uom_qty": qty_returned,
                        "qty_delivered": qty_returned,
                        "qty_returned": qty_returned,
                        "rental_return_date": wizard_line.return_date,
                    }
                )
        return res
