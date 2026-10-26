# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    phase_id = fields.Many2one("project.task.phase", inverse="_inverse_phase_id")

    @api.depends("phase_id", "sale_line_id")
    def _compute_estimate_id(self):
        for task in self:
            if task.phase_id and task.project_id:
                domain = [
                    ("phase_id", "=", task.phase_id.id),
                    ("project_id", "=", task.project_id.id),
                    ("is_in_progress", "=", True),
                ]
                if task.sale_line_id:
                    domain.append(("sale_line_id", "=", task.sale_line_id.id))
                estimate_id = self.env["project.estimate"].search(domain)[:1]
                if not estimate_id:
                    vals = {
                        "project_id": task.project_id.id,
                        "phase_id": task.phase_id.id,
                        "planned_hours": 0.0,
                    }
                    if task.sale_line_id:
                        vals["sale_line_id"] = task.sale_line_id.id
                    estimate_id = self.env["project.estimate"].create(vals)
                task.estimate_id = estimate_id
            else:
                task.estimate_id = False

    def _inverse_phase_id(self):
        """
        Set the sale line if phase with estimate is selected.
        """
        for task in self:
            estimate_ids = task.phase_id.estimate_ids.filtered(lambda est: est.project_id == task.project_id)
            if estimate_ids and not task.sale_line_id:
                estimate_id = estimate_ids.filtered(lambda est: est.sale_line_id and est.is_in_progress)[:1]
                if estimate_id:
                    task.sale_line_id = estimate_id.sale_line_id
