import logging
from datetime import date, datetime, timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

from .config import DURATION_SELECTION


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_from = fields.Date(
        string="Start Date",
        required=True,
        help="Start Date of Patent",
        default=fields.Date.today(),
    )

    date_to = fields.Date(compute="_compute_date_to")

    # @api.onchange("product_id")
    # def _onchange_product_id_date_from(self):
    #     for line in self:
    #         if not line.product_id:
    #             continue

    #         if line.product_id.duration == "year":
    #             today = fields.Date.context_today(line)
    #             october_1 = date(today.year, 10, 1)

    #             year = today.year + 1 if today > october_1 else today.year
    #             line.date_from = datetime(year, 1, 1)
    #         else:
    #             line.date_from = fields.Datetime.now()
    #
    @api.constrains("product_id", "date_from", "order_id.partner_id")
    def _check_permit_limits(self):
        # limits per duration
        limits = {
            "year": 1,
            "week": 2,
            "day": 5,
        }

        for line in self:
            if not line.product_id or not line.date_from:
                continue

            duration = line.product_id.duration

            if duration not in limits:
                continue

            partner = line.order_id.partner_id
            if not partner:
                continue

            year = line.date_from.year

            date_start = date(year, 1, 1)
            date_end = date(year, 12, 31)

            domain = [
                ("id", "!=", line.id),
                ("product_id.duration", "=", duration),
                ("date_from", ">=", date_start),
                ("date_from", "<=", date_end),
                ("order_id.partner_id", "=", partner.id),
                ("order_id.state", "in", ["sale", "done"]),
            ]

            count = self.search_count(domain)

            # include the current line
            if count + 1 > limits[duration]:
                raise ValidationError(
                    _(
                        "This customer already reached the limit for %s permits "
                        "for year %s (maximum: %s)."
                    )
                    % (duration, year, limits[duration])
                )

    @api.onchange("date_from", "product_id")
    def _onchange_date_from_year(self):
        for line in self:
            if (
                line.date_from
                and line.product_id
                and line.product_id.duration == "year"
            ):
                line.date_from = line.date_from.replace(
                    month=1,
                    day=1,
                )

    # @api.depends("date_from")
    # def _compute_date_to(self):
    #     duration_map = {
    #         "year": {"days": 365},
    #         "day": {"days": 1},
    #         "week": {"weeks": 1},
    #     }
    #     for line in self:
    #         if not line.date_from or not line.product_id:
    #             line.date_to = line.date_from
    #             continue

    #         duration = line.product_id.duration

    @api.depends("date_from", "product_id.duration")
    def _compute_date_to(self):
        for line in self:
            if not line.date_from or not line.product_id:
                line.date_to = line.date_from
                continue

            duration = line.product_id.duration

            if duration == "day":
                if not self._check_valid_date(line.date_from):
                    continue

                line.date_to = line.date_from
                continue

            if duration == "year":
                line.date_to = line.date_from.replace(
                    month=12,
                    day=31,
                )
                continue

            if duration == "week":
                current_date = line.date_from
                valid_days = 0

                while valid_days < 7:
                    current_date += timedelta(days=1)

                    # Skip non valid days
                    if not self._check_valid_date(current_date):
                        continue

                    valid_days += 1

                line.date_to = current_date - timedelta(days=1)
            else:
                line.date_to = line.date_from

    def _check_valid_date(self, date):
        today = fields.Date.today()
        country = "Schweiz"

        calendars = (
            self.env["calendar.public.holiday"]
            .sudo()
            .search(
                [
                    ("year", ">=", today.year),
                    ("country_id.name", "=", country),
                ]
            )
        )

        public_holidays = calendars.mapped("line_ids.date")

        if date.weekday() == 6 or date in public_holidays:
            return False
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            date_from = vals.get("date_from")
            product_id = vals.get("product_id")
            product = self.env["product.template"].browse(product_id)
            if date_from and product:
                vals["date_from"] = self._normalize_date_from(
                    date_from, product.duration
                )
        return super().create(vals_list)

    # def write(self, vals):
    #     if "date_from" in vals or "product_id" in vals:
    #         date_from = vals.get("date_from")
    #         product_id = vals.get("product_id")
    #         product = self.env["product.template"].browse(product_id) or self.product_id

    #         vals["date_from"] = self._normalize_date_from(date_from, product.duration)

    #     return super().write(vals)

    def write(self, vals):
        if "date_from" in vals or "product_id" in vals:
            new_vals = []
            for line in self:
                v = dict(vals)

                product_id = v.get("product_id", line.product_id.id)
                date_from = v.get("date_from", line.date_from)

                if product_id and date_from:
                    product = self.env["product.product"].browse(product_id)

                    if product.duration == "year":
                        if isinstance(date_from, str):
                            date_from = fields.Date.from_string(date_from)

                        v["date_from"] = date_from.replace(
                            month=1,
                            day=1,
                        )

                new_vals.append(v)

            # IMPORTANT: write multi with possibly different vals
            for line, v in zip(self, new_vals):
                super(SaleOrderLine, line).write(v)
            return True

        return super().write(vals)

    def _normalize_date_from(self, date_from, duration):
        if duration == "year":
            date_from = date_from.replace(
                month=1,
                day=1,
            )
        return date_from
