# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProjectEstimate(models.Model):
    _inherit = "project.estimate"

    sale_line_id = fields.Many2one("sale.order.line")

    @api.constrains("project_id", "phase_id", "is_in_progress", "sale_line_id")
    def _check_project_phase_unique(self):
        for estimate in self:
            if not estimate.phase_id or not estimate.is_in_progress:
                continue
            if estimate.project_id:
                # Unique by project_id + phase_id + is_in_progress
                domain = [
                    ("project_id", "=", estimate.project_id.id),
                    ("phase_id", "=", estimate.phase_id.id),
                    ("is_in_progress", "=", True),
                    ("id", "!=", estimate.id),
                ]
            elif estimate.sale_line_id:
                # Unique by phase_id + is_in_progress + sale_line_id (no project)
                domain = [
                    ("phase_id", "=", estimate.phase_id.id),
                    ("is_in_progress", "=", True),
                    ("sale_line_id", "=", estimate.sale_line_id.id),
                    ("id", "!=", estimate.id),
                ]
            else:
                continue
            duplicate = self.search(domain, limit=1)
            if duplicate:
                raise ValidationError(
                    "Only one estimate per project or sale order line and phase can be in progress at a time."
                )

    sale_order_id = fields.Many2one("sale.order", related="sale_line_id.order_id")
    partner_id = fields.Many2one("res.partner", related="project_id.partner_id")

    planned_hours = fields.Float(inverse="_inverse_planned_hours")

    def _inverse_planned_hours(self):
        for estimate in self:
            estimate_ids = self.search([("sale_line_id", "=", estimate.sale_line_id.id)])
            estimate.sale_line_id.product_uom_qty = sum(estimate_ids.mapped("planned_hours"))
