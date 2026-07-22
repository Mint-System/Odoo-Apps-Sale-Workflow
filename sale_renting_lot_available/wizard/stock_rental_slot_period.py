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
        Search for slot with lots in time range.
        Apply filter that hides these slots.
        """
        self.ensure_one()
        view_mode = self.env.context.get("view_mode", "gantt")
        # FIXME
        # domain = [
        #     "|",
        #     ("return_date", "<", self.start_date),
        #     ("start_date", ">", self.return_date),
        # ]
        context = {
            "search_default_groupby_product": 1,
            "search_default_groupby_lot": 1,
        }
        view_modes = f"{view_mode},list,form" if view_mode != "list" else "list,form"
        return {
            "type": "ir.actions.act_window",
            "name": "Rental Slots",
            "res_model": "stock.rental.slot",
            "view_mode": view_modes,
            "domain": domain,
            "context": context,
        }
