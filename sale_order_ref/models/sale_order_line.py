# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def name_get(self):
        """
        Overwrite: Return display name with order ref.
        """
        result = []
        for so_line in self.sudo():
            name = "%s - %s" % (
                so_line.order_id.name,
                so_line.name and so_line.name.split("\n")[0] or so_line.product_id.name,
            )
            ref = so_line.order_id.ref
            if ref:
                name = "%s (%s) - %s" % (
                    so_line.order_id.name,
                    ref,
                    so_line.product_id.name,
                )
            if so_line.order_partner_id.ref:
                name = "%s (%s)" % (name, so_line.order_partner_id.ref)
            result.append((so_line.id, name))
        return result
