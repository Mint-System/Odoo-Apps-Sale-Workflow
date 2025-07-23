import datetime
import logging

from odoo import _, fields, models
from odoo.tools import format_date
from odoo.tools.date_utils import get_timedelta

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        """
        If it is the first invoice update the start and end date.
        """
        res = super()._prepare_invoice_line(**optional_values)

        # Check if no unpaid invoices exist.
        invoice_line_count = len(
            self.invoice_lines.filtered(
                lambda l: l.move_type == "out_invoice" and l.move_id.payment_state not in ["not_paid", "reversed"]
            )
        )

        # Ensure order is recurring
        if invoice_line_count == 0 and (
            self.temporal_type == "subscription" or self.order_id.subscription_management == "upsell"
        ):
            lang_code = self.order_id.partner_id.lang

            # The end_date is always the end of the year set in next_invoice_date
            next_invoice_date = self.order_id.next_invoice_date
            end_date = datetime.date(next_invoice_date.year, 12, 31)
            format_end_date = format_date(self.env, end_date, lang_code=lang_code)

            # If the start_date older than the year in next_invoice_date, set it
            # to the beginning of the year in next_invoice_date.
            start_date = self.order_id.start_date
            if start_date.year != next_invoice_date.year:
                start_date = datetime.date(next_invoice_date.year, 1, 1)
            format_start_date = format_date(self.env, start_date, lang_code=lang_code)

            description = "%s - %s" % (
                self.name,
                self.order_id.recurrence_id.duration_display,
            )
            description += _("\n%s to %s", format_start_date, format_end_date)
            res.update(
                {
                    "name": description,
                    "subscription_start_date": start_date,
                    "subscription_end_date": datetime.date(fields.Date.today().year + 1, 12, 31)
                    - get_timedelta(
                        self.order_id.recurrence_id.duration,
                        self.order_id.recurrence_id.unit,
                    ),
                }
            )
        return res
