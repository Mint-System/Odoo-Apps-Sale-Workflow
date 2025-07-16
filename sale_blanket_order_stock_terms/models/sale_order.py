import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        res = super().create(vals)

        # Copy incoterm and shipping policy
        if res.blanket_order_id:
            if res.blanket_order_id.incoterm:
                res.incoterm = res.blanket_order_id.incoterm
            if res.blanket_order_id.incoterm:
                res.picking_policy = res.blanket_order_id.picking_policy

        return res
