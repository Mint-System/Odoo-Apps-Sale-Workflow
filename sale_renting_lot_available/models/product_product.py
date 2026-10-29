# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    stock_rental_slot_ids = fields.One2many(
        "stock.rental.slot",
        "product_id",
        string="Rental Slots",
    )

    def _generate_stock_rental_lot(self):
        """
        Delete linked placeholder slots and create one for each qty
        for untracked storable rental products.
        """
        for product in self.filtered(lambda p: p.rent_ok and p.is_storable and p.tracking == "none"):
            product.stock_rental_slot_ids.filtered("is_placeholder").sudo().unlink()
            qty = int(product.qty_available)
            for _ in range(qty):
                self.env["stock.rental.slot"].create({"product_id": product.id})
