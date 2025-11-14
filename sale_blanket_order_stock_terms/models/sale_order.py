import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)

        for order in orders:
            if order.blanket_order_id:
                if order.blanket_order_id.incoterm:
                    order.incoterm = order.blanket_order_id.incoterm
                if order.blanket_order_id.picking_policy:
                    order.picking_policy = order.blanket_order_id.picking_policy

        return orders
