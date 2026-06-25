# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class StockRentalSlotPeriod(models.TransientModel):
    _name = "stock.rental.slot.period"
    _description = "Stock Rental Slot Period"

    start_date = fields.Datetime(required=True, default=fields.Datetime.now)
    return_date = fields.Datetime(required=True, default=fields.Datetime.now)

    def action_apply(self):
        self.ensure_one()
        domain = [
            ("start_date", "<=", self.return_date),
            ("return_date", ">=", self.start_date),
        ]
        return {
            "type": "ir.actions.act_window",
            "name": "Rental Slots",
            "res_model": "stock.rental.slot",
            "view_mode": "gantt,list,form",
            "domain": domain,
        }
