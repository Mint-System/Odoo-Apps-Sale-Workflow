# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

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
