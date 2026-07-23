# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from datetime import timedelta

from odoo import models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_active_rental_lines(self, from_date, to_date, ignored_soline_id=False, warehouse_id=False, **kwargs):
        """
        Overwrite: Use rental_return_date instead of return_date.
        """

        domain = [
            ("is_rental", "=", True),
            ("product_id", "=", self.id),
            ("state", "=", "sale"),
        ]

        if ignored_soline_id:
            domain += [("id", "!=", ignored_soline_id)]

        if warehouse_id:
            domain += [("order_id.warehouse_id", "=", warehouse_id)]

        include_bounds = to_date == from_date
        domain += [
            ("rental_return_date", ">=" if include_bounds and not kwargs.get("rental_pivot_date") else ">", from_date),
            "|",
            (
                "reservation_begin",
                "<=" if include_bounds else "<",
                to_date - timedelta(hours=self.preparation_time if kwargs.get("rental_pivot_date") else 0),
            ),
            ("qty_delivered", ">", 0),
        ]

        return self.env["sale.order.line"].search(domain)
