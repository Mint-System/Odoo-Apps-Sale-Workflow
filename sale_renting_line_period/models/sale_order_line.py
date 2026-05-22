# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from math import ceil

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    rental_start_date = fields.Datetime(string="Rental Start Date", compute="_compute_rental_period", store=True)
    rental_return_date = fields.Datetime(string="Rental Return Date", compute="_compute_rental_period", store=True)
    duration_days = fields.Integer(
        string="Duration in days",
        compute="_compute_duration",
        help="The duration in days of the rental period.",
    )
    remaining_hours = fields.Integer(
        string="Remaining duration in hours",
        compute="_compute_duration",
        help="The leftover hours of the rental period.",
    )
    rental_status = fields.Selection(
        selection=[
            ("pickup", "Booked"),
            ("return", "Delivered"),
            ("returned", "Returned"),
        ],
        compute="_compute_rental_status",
    )
    next_action_date = fields.Datetime(string="Next Action", compute="_compute_rental_status", store=True)

    @api.depends("order_id.rental_start_date", "order_id.rental_return_date")
    def _compute_rental_period(self):
        """
        Copy rental start and return date if:
        - Product is rental
        - Either one is not set
        - Dates are equal to the current value
        """
        for line in self.filtered("is_rental"):
            original_start_date = line.order_id._origin.rental_start_date.date()
            original_return_date = line.order_id._origin.rental_return_date.date()
            start_date = line.order_id._origin.rental_start_date.date() or False
            return_date = line.order_id._origin.rental_return_date.date() or False
            _logger.warning([original_start_date, start_date, original_return_date, return_date])
            if not start_date or (original_start_date == start_date):
                line.rental_start_date = line.order_id.rental_start_date
            if not return_date or (original_return_date == return_date):
                line.rental_return_date = line.order_id.rental_return_date

    @api.depends("rental_start_date", "rental_return_date")
    def _compute_duration(self):
        self.duration_days = 0
        self.remaining_hours = 0
        for line in self:
            if line.rental_start_date and line.rental_return_date:
                duration = line.rental_return_date - line.rental_start_date
                line.duration_days = duration.days
                line.remaining_hours = ceil(duration.seconds / 3600)

    @api.depends(
        "rental_start_date",
        "rental_return_date",
        "state",
        "is_rental",
        "product_uom_qty",
        "qty_delivered",
        "qty_returned",
    )
    def _compute_rental_status(self):
        self.next_action_date = False
        for line in self:
            if not line.is_rental:
                line.rental_status = False
            elif line.qty_returned < line.qty_delivered:
                line.rental_status = "return"
                line.next_action_date = line.rental_return_date
            elif line.qty_delivered < line.product_uom_qty:
                line.rental_status = "pickup"
                line.next_action_date = line.rental_start_date
            else:
                line.rental_status = "returned"
