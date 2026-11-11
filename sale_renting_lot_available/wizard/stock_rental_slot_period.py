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

    def get_available_slot_ids(self):
        """
        Return placeholder slots that are available in the time range.

        Available slots are the placeholder slots minus the maximum number of
        booked slots that overlap in the time range.
        """
        available_slot_ids = []

        # Group placeholder slots by product using the ORM
        groups = self.env["stock.rental.slot"]._read_group(
            domain=[
                ("is_placeholder", "=", True),
                ("company_id", "=", self.env.company.id),
            ],
            groupby=["product_id"],
            aggregates=["id:recordset"],
        )

        for product, _group_placeholder_slot_ids in groups:
            available_slot_ids += (
                self.env["stock.rental.slot"]
                ._get_available_placeholder_slot_ids(product, self.start_date, self.end_date, self.env.company)
                .ids
            )

        return available_slot_ids

    def action_view_available_slots(self):
        """
        Show placeholder slots minus the sale order slots in range.
        """
        self.ensure_one()
        self.action_adjust_period()
        available_slot_ids = self.get_available_slot_ids()
        return {
            "type": "ir.actions.act_window",
            "name": "Rental Slots",
            "res_model": "stock.rental.slot",
            "view_mode": "list,form",
            "domain": [("id", "in", available_slot_ids)],
            "context": {
                "search_default_groupby_category": 1,
                "search_default_groupby_product": 1,
                "default_rental_start_date": self.start_date,
                "default_rental_return_date": self.end_date,
            },
        }

    def action_adjust_period(self):
        """
        Update placeholder slots with start and end date.
        """
        self.ensure_one()

        # Get all placeholder slots and update dates.
        start_placeholder_slot_ids = self.env["stock.rental.slot"].search(
            [
                ("is_placeholder", "=", True),
                "|",
                ("lot_id.start_slot_id", "!=", False),
                ("lot_id", "=", False),
                ("company_id", "=", self.env.company.id),
            ]
        )
        start_placeholder_slot_ids.write({"start_date": self.start_date, "return_date": self.start_date})

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
