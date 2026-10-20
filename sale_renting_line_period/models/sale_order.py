# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Color index for the order-level ``rental_status`` badge in the rental
    # order list. Mirrors the palette mapping used elsewhere; keep in sync.
    rental_status_color = fields.Integer(
        string="Rental Color",
        compute="_compute_rental_status_color",
    )

    _rental_status_colors = {
        False: 10,
        "draft": 10,
        "sent": 10,
        "pickup": 5,
        "return": 2,
        "returned": 0,
        "cancel": 0,
    }

    @api.depends("rental_status")
    def _compute_rental_status_color(self):
        for order in self:
            order.rental_status_color = self._rental_status_colors.get(order.rental_status, 10)

    def action_cancel(self):
        """
        Prevent cancel if lots are not returned.
        """
        res = super().action_cancel()
        for order in self:
            if order.order_line.filtered(lambda l: l.rental_status == "return"):
                raise UserError(
                    _("Rental order '%s' cannot be cancelled. It has order lines in rental state 'return'.", order.name)
                )
        return super().action_cancel()
