# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    @api.depends("order_partner_id", "order_id", "product_id")
    def _compute_display_name(self):
        super()._compute_display_name()
        for so_line in self.sudo():
            so_line.display_name = f"{so_line.display_name}"


    def _additional_name_per_id(self):
        return {}