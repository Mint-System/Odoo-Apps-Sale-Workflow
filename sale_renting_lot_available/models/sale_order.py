# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    rental_slot_count = fields.Integer(
        compute="_compute_rental_slot_count",
        string="Rental Slots",
    )

    @api.depends("order_line.rental_slot_ids")
    def _compute_rental_slot_count(self):
        for order in self:
            order.rental_slot_count = len(order.mapped("order_line.rental_slot_ids"))

    def action_confirm(self):
        """Create slots when order is confirmed."""
        res = super().action_confirm()
        self.order_line._create_stock_rental_lot()
        return res

    def action_cancel(self):
        """Unlink slots when order is cancelled."""
        res = super().action_cancel()
        self.order_line.rental_slot_ids.sudo().unlink()
        return super().action_cancel()

    def action_view_rental_slots(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Rental Slots"),
            "res_model": "stock.rental.slot",
            "view_mode": "gantt,list,form",
            "context": {
                "search_default_sale_order_id": self.id,
            },
        }

    def unlink(self):
        self.order_line.rental_slot_ids.sudo().unlink()
        return super().unlink()
