# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ref = fields.Char("Internal Reference", copy=False)

    @api.depends("ref")
    def _compute_display_name(self):
        for rec in self:
            if rec.ref:
                rec.display_name = rec.name + f" ({rec.ref})"
            else:
                rec.display_name = rec.name
