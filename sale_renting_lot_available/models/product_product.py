# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    rental_slot_count = fields.Integer(
        compute="_compute_rental_slot_count",
        string="Rental Slots",
    )

    @api.depends("stock_rental_slot_ids")
    def _compute_rental_slot_count(self):
        for product in self:
            product.rental_slot_count = len(product.stock_rental_slot_ids)

    def action_view_rental_slots(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Rental Slots"),
            "res_model": "stock.rental.slot",
            "view_mode": "gantt,list,form",
            "context": {
                "search_default_product_id": self.id,
                "search_default_groupby_product": 1,
                "search_default_groupby_lot": 1,
            },
        }
