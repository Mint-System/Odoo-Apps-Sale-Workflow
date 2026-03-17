# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProjectEstimate(models.Model):
    _inherit = "project.estimate"

    sale_line_id = fields.Many2one("sale.order.line")
    sale_order_id = fields.Many2one("sale.order", related="sale_line_id.order_id")
    partner_id = fields.Many2one("res.partner", related="project_id.partner_id")

    planned_hours = fields.Float(inverse="_inverse_planned_hours")

    def _inverse_planned_hours(self):
        for estimate in self:
            estimate_ids = self.search([("sale_line_id", "=", estimate.sale_line_id.id)])
            estimate.sale_line_id.product_uom_qty = sum(estimate_ids.mapped("planned_hours"))
