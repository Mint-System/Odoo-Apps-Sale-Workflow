# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from math import ceil

from pytz import UTC, timezone

from odoo import _, api, fields, models
from odoo.tools import format_date

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    _rental_period_coherence = models.Constraint(
        "CHECK(rental_start_date < rental_return_date)",
        "The rental start date must be before the rental return date if any.",
    )

    rental_start_date = fields.Datetime(
        string="Rental Start Date", compute="_compute_rental_period", precompute=True, store=True, readonly=False
    )
    rental_return_date = fields.Datetime(
        string="Rental Return Date", compute="_compute_rental_period", precompute=True, store=True, readonly=False
    )
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
    same_product_line_ids = fields.One2many("sale.order.line", compute="_compute_same_product_line_ids")

    @api.depends("product_id", "order_id.rental_start_date", "order_id.rental_return_date")
    def _compute_rental_period(self):
        """
        Copy rental start and return date if:
        - Product is rental
        - The is not set
        - Status is not returned
        """
        for line in self:
            if line.is_rental:
                if not line.rental_start_date or line.rental_status != "returned":
                    line.rental_start_date = line.order_id.rental_start_date
                if not line.rental_return_date or line.rental_status != "returned":
                    line.rental_return_date = line.order_id.rental_return_date
            else:
                line.rental_start_date = False
                line.rental_return_date = False

    @api.depends("rental_start_date", "rental_return_date")
    def _compute_name(self):
        """
        Override to add the compute dependency.
        """
        super()._compute_name()

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
            # Next action is return
            elif line.qty_returned < line.qty_delivered:
                line.rental_status = "return"
                line.next_action_date = line.rental_return_date
            # Ready to deliver
            elif line.qty_delivered < line.product_uom_qty:
                line.rental_status = "pickup"
                line.next_action_date = line.rental_start_date
            else:
                line.rental_status = "returned"

    def _compute_same_product_line_ids(self):
        for line in self:
            line.same_product_line_ids = line.order_id.order_line.filtered(
                lambda l: l.id != line.id and l.product_id == line.product_id
            )

    def _get_rental_order_line_description(self):
        """
        Use start and return date from order line.
        Format without time.
        """
        tz = self._get_tz()
        start_date = self.rental_start_date
        return_date = self.rental_return_date
        env = self.with_context(use_babel=True).env

        if (
            start_date
            and return_date
            and start_date.replace(tzinfo=UTC).astimezone(timezone(tz)).date()
            == return_date.replace(tzinfo=UTC).astimezone(timezone(tz)).date()
        ):
            return_date_part = format_date(env, return_date)
        else:
            return_date_part = format_date(env, return_date)
        start_date_part = format_date(env, start_date)
        return _("\n%(from_date)s to %(to_date)s", from_date=start_date_part, to_date=return_date_part)

    @api.depends(
        "product_id",
        "rental_start_date",
        "rental_return_date",
        "order_id.pricelist_id",
    )
    def _compute_price_unit(self):
        super()._compute_price_unit()

        for line in self.filtered(lambda l: l.is_rental and l.rental_start_date and l.rental_return_date):
            pricing = line.product_id.product_tmpl_id._get_best_pricing_rule(
                product=line.product_id,
                start_date=line.rental_start_date,
                end_date=line.rental_return_date,
                pricelist=line.order_id.pricelist_id,
                currency=line.currency_id,
                company=line.company_id,
            )
            if not pricing:
                continue

            duration_vals = self.env["product.pricing"]._compute_duration_vals(
                line.rental_start_date,
                line.rental_return_date,
            )
            unit = pricing.recurrence_id.unit
            price = pricing._compute_price(duration_vals[unit], unit)

            if pricing.currency_id != line.currency_id:
                price = pricing.currency_id._convert(
                    from_amount=price,
                    to_currency=line.currency_id,
                    company=line.company_id,
                    date=fields.Date.today(),
                )

            line.price_unit = price

    def action_split_line(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("sale_renting_line_period.rental_order_line_wizard_action")
        action["context"] = {
            "default_so_line_id": self.id,
        }
        return action
