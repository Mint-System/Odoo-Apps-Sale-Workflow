# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class StockRentalSlotPeriod(models.TransientModel):
    _name = "stock.rental.slot.period"
    _description = "Stock Rental Slot Period"

    start_date = fields.Datetime(required=True, default=fields.Datetime.now)
    return_date = fields.Datetime(required=True, default=fields.Datetime.now)

    def action_view_gantt_or_list(self):
        """
        Update placeholder slots with start date.
        """
        self.ensure_one()

        # Get all placeholder slots and update.
        placeholder_lot_ids = self.env["stock.rental.slot"].search([("is_placeholder", "=", True)])
        placeholder_lot_ids.write({"start_date": self.start_date,"return_date": self.start_date})

        view_mode = self.env.context.get("view_mode", "gantt")
        view_modes = f"{view_mode},list,form" if view_mode != "list" else "list,form"
        return {
            "type": "ir.actions.act_window",
            "name": "Rental Slots",
            "res_model": "stock.rental.slot",
            "view_mode": view_modes,
            "domain": [],
            "context": {
                "search_default_groupby_product": 1,
                "search_default_groupby_lot": 1,
            },
        }
