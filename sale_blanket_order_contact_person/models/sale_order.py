import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        res = super().create(vals)

        # Copy contact person if blanket order is passed
        if res.blanket_order_id:
            res.partner_sale_id = res.blanket_order_id.partner_sale_id

        return res
