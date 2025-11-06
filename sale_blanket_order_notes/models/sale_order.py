import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        sale_order = super().create(vals)

        # Copy note fields from blanket order
        if sale_order.blanket_order_id:
            sale_order.note_header = sale_order.blanket_order_id.note_header
            sale_order.note_footer = sale_order.blanket_order_id.note_footer

        return sale_order
