import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        super()._action_confirm()
        for order in self:
            order.partner_id._compute_product_pricelist()

    def _action_cancel(self):
        super()._action_cancel()
        for order in self:
            order.partner_id._compute_product_pricelist()
