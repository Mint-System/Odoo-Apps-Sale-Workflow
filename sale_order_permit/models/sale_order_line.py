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

    @api.onchange("product_id")
    def _onchange_product_id_date_from(self):
        for line in self:
            if not line.product_id:
                continue

            if line.product_id.duration == "year":
                today = fields.Date.context_today(line)
                october_1 = date(today.year, 10, 1)

                year = today.year + 1 if today > october_1 else today.year
                line.date_from = datetime(year, 1, 1)
            else:
                line.date_from = fields.Datetime.now()

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
                line.date_to = line.date_from + timedelta(days=1)
                continue

            if duration == "year":
                line.date_to = line.date_from + timedelta(days=365)
                continue

            if duration == "week":
                current_date = line.date_from
                today = fields.Date.today()

                valid_days = 0
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

                while valid_days < 7:
                    current_date += timedelta(days=1)

                    # Skip Sundays
                    if current_date.weekday() == 6:
                        continue

                    # Skip public holidays
                    if current_date in public_holidays:
                        continue

                    valid_days += 1

                line.date_to = current_date - timedelta(days=1)
            else:
                line.date_to = line.date_from

            # _logger.warning(f"duration: {duration}")
            # if line.date_from and line.product_id.duration in duration_map.keys():
            #    line.date_to = line.date_from + timedelta(**duration_map[duration])
            # else:
            #     line.date_to = line.date_from
