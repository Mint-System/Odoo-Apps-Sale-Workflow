import datetime
import logging

from odoo import _, fields, models
from odoo.tools import format_date
from odoo.tools.date_utils import get_timedelta

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        """If is first invoice update the start and end date."""
        res = super()._prepare_invoice_line(**optional_values)
        if self.order_id.invoice_count == 0 and (
            self.temporal_type == "subscription"
            or self.order_id.subscription_management == "upsell"
        ):
            lang_code = self.order_id.partner_id.lang
            start_date = self.order_id.start_date
            format_start_date = format_date(self.env, start_date, lang_code=lang_code)
            end_date = datetime.date(fields.Date.today().year + 1, 12, 31)
            format_end_date = format_date(self.env, end_date, lang_code=lang_code)

            description = "%s - %s" % (
                self.name,
                self.order_id.recurrence_id.duration_display,
            )
            description += _("\n%s to %s", format_start_date, format_end_date)
            res.update(
                {
                    "name": description,
                    "subscription_start_date": start_date,
                    "subscription_end_date": end_date
                    - get_timedelta(
                        self.order_id.recurrence_id.duration,
                        self.order_id.recurrence_id.unit,
                    ),
                }
            )
        return res
