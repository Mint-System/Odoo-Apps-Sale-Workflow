# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrderLineWizard(models.TransientModel):
    _name = "rental.order.line.wizard"
    _description = "Rental Order Line Wizard"

    so_line_id = fields.Many2one("sale.order.line")
    qty_diff = fields.Float()
    product_uom_qty = fields.Float(related="so_line_id.product_uom_qty", readonly=True)

    def split(self):
        """
        Duplicate sale order line.
        The qty diff is subtracted on current line and set on new line.
        """
        self.ensure_one()

        if self.so_line_id.rental_status in ["return", "returned"]:
            raise UserError(
                _(
                    "Cannot split line with product '%s'. Only lines in draft and pickup can be splitted.",
                    self.so_line_id.product_id.name,
                )
            )

        if self.qty_diff <= 0 or self.qty_diff >= self.product_uom_qty:
            raise UserError(
                _(
                    "Cannot split line with product '%s'. Qty diff must be strictly between 0 and %s.",
                    self.so_line_id.product_id.name,
                    self.product_uom_qty,
                )
            )

        self.so_line_id.product_uom_qty -= self.qty_diff
        new_line = self.so_line_id.copy(default={"product_uom_qty": self.qty_diff})

        return new_line
