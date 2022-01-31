from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.customer_lead', 'date_order', 'order_line.state')
    def _compute_expected_date(self):
        super()._compute_expected_date()
        for order in self:
            if not order.commitment_date:
                order.commitment_date = order.expected_date

    def copy(self, default=None):
        res = super().copy(default=default)
        res._compute_expected_date()
        return res
