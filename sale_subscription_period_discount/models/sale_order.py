import datetime
import logging

from odoo import models, api, fields
from odoo.tools.date_utils import get_timedelta

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        """Apply period discount if start date is greater than virtual last invoice date."""
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        for move in moves:
            order = move.line_ids.sale_line_ids.order_id[:1]
            last_virtual_invoice_date = order.next_invoice_date - get_timedelta(
                order.recurrence_id.duration, order.recurrence_id.unit
            )
            if (
                order
                and order.start_date
                and (last_virtual_invoice_date < order.start_date)
            ):
                period_discount = order.recurrence_id.get_period_discount(
                    date=order.start_date
                )
                if period_discount:
                    move.line_ids.write({"discount": period_discount.discount})
        return moves

    @api.depends("is_subscription", "state", "start_date", "subscription_management")
    def _compute_next_invoice_date(self):
        for so in self:
            if (
                so.is_subscription
                and not so.next_invoice_date
            ):
                so.next_invoice_date = datetime.date(
                    fields.Date.today().year+1, 1, 1
                )
        return super()._compute_next_invoice_date()
