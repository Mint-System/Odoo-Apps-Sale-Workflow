# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from dateutil.relativedelta import relativedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)


class StockRentalSlotPeriod(models.TransientModel):
    _name = "stock.rental.slot.period"
    _description = "Stock Rental Slot Period"

    start_date = fields.Datetime(required=True, default=fields.Datetime.now)
    end_date = fields.Datetime(required=True, default=lambda self: fields.Datetime.now() + relativedelta(months=1))

    def action_view_available_slots(self):
        """
        Show placeholder slots minus the sale order slots in range.
        """
        self.ensure_one()
        action = self.action_adjust_period()
        available_slot_ids = []

        # Group placeholder slots by product using the ORM
        groups = self.env["stock.rental.slot"]._read_group(
            domain=[("is_placeholder", "=", True)],
            groupby=["product_id"],
            aggregates=["id:recordset"],
        )

        # For each group check if there are non placeholder (sale order) slots
        for product, group_placeholder_slot_ids in groups:
            _logger.warning([product, group_placeholder_slot_ids])
            sale_order_slot_count = self.env["stock.rental.slot"].search_count(
                [
                    ("is_placeholder", "=", False),
                    ("product_id", "=", product.id),
                    ("start_date", "<=", self.end_date),
                    ("return_date", ">=", self.start_date),
                ]
            )
            # Remove as many placeholders as there are booked slots; the rest are available
            available_slot_ids += group_placeholder_slot_ids[sale_order_slot_count:].ids

        return {
            "type": "ir.actions.act_window",
            "name": "Rental Slots",
            "res_model": "stock.rental.slot",
            "view_mode": "list,form",
            "domain": [("id", "in", available_slot_ids)],
            "context": {
                "search_default_groupby_category": 1,
                "search_default_groupby_product": 1,
            },
        }

    def action_adjust_period(self):
        """
        Update placeholder slots with start and end date.
        """
        self.ensure_one()

        # Get all placeholder slots and update dates.
        start_placeholder_lot_ids = self.env["stock.rental.slot"].search(
            [("is_placeholder", "=", True), ("lot_id.start_slot_id", "!=", False)]
        )
        start_placeholder_lot_ids.write({"start_date": self.start_date, "return_date": self.start_date})
        # end_placeholder_lot_ids = self.env["stock.rental.slot"].search(
        #     [("is_placeholder", "=", True), ("lot_id.end_slot_id", "!=", False)]
        # )
        # end_placeholder_lot_ids.write({"start_date": self.end_date, "return_date": self.end_date})

        return {
            "type": "ir.actions.act_window",
            "name": "Rental Slots",
            "res_model": "stock.rental.slot",
            "view_mode": "gantt,form",
            "domain": [],
            "context": {
                "search_default_groupby_product": 1,
                "search_default_groupby_lot": 1,
            },
        }
