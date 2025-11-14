import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        """
        Write owner after confirmation.
        """
        res = super()._action_confirm()
        for order in self:
            pickings = order.picking_ids.filtered(lambda x: x.picking_type_code == "outgoing")
            pickings.write({"owner_id": order.partner_id.id})
        return res
