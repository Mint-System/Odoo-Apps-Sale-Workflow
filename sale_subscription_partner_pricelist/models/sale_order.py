import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # @api.depends("stage_category", "state", "is_subscription", "amount_untaxed")
    def _compute_recurring_monthly(self):
        super()._compute_recurring_monthly()
        for order in self:
            order.partner_id._compute_product_pricelist()
