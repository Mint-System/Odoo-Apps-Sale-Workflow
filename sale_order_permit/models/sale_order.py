import logging
from datetime import timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()

        seq = self.env.ref("sale_order_permit.seq_permit_number")
        for order in self:
            if not order.partner_id.permit_number:
                order.partner_id.permit_number = seq.next_by_id()

        return res
