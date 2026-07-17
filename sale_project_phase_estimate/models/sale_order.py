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
