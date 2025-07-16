import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    name = fields.Text(compute="_compute_name", store=True)

    @api.depends("product_id")
    def _compute_name(self):
        for line in self:
            if line.product_id and line.name:
                if line.product_id.display_name and line.product_id.name:
                    line.name = line.name.replace(line.product_id.display_name, line.product_id.name)
            elif line.product_id and not line.name:
                line.name = line.product_id.name
            else:
                line.name = ""
