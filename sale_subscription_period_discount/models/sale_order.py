import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    start_date = fields.Date(copy=False)

    def _create_invoices(self, grouped=False, final=False, date=None):
        """Apply period discount if start date is greater than virtual last invoice date."""
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        for move in moves:
            order = move.line_ids.sale_line_ids.order_id[:1]
            if order and order.start_date and order.invoice_count <= 1:
                period_discount = order.recurrence_id.get_period_discount(date=order.start_date)
                if period_discount:
                    move.line_ids.write({"discount": period_discount.discount})
        return moves
