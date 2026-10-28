# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    estimate_ids = fields.One2many(
        "project.estimate", "sale_order_id", compute="_compute_estimate_ids", store=True, readonly=False
    )

    @api.depends("order_line.estimate_ids")
    def _compute_estimate_ids(self):
        for order in self:
            order.estimate_ids = order.order_line.mapped("estimate_ids")

    def toggle_active(self):
        """Archive or restore the estimates linked to the order together with it."""
        previous_active = {order.id: order.active for order in self}
        super().toggle_active()
        for order in self:
            estimate_ids = order.with_context(active_test=False).order_line.mapped("estimate_ids")
            if not estimate_ids:
                continue
            if previous_active.get(order.id) and not order.active:
                estimate_ids.active = False
            elif not previous_active.get(order.id) and order.active:
                estimate_ids.active = True
