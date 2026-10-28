# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    phase_id = fields.Many2one("project.task.phase", inverse="_inverse_phase_id")

    @api.depends("phase_id", "project_id", "sale_line_id")
    def _compute_estimate_id(self):
        """Link the task to an existing estimate matching phase, project and sale line.

        Estimates are never created here, they can only be selected from the sale
        order or the estimate list.
        """
        for task in self:
            if task.phase_id and task.project_id:
                domain = [
                    ("phase_id", "=", task.phase_id.id),
                    ("project_id", "=", task.project_id.id),
                    ("is_in_progress", "=", True),
                ]
                if task.sale_line_id:
                    domain.append(("sale_line_id", "=", task.sale_line_id.id))
                task.estimate_id = self.env["project.estimate"].search(domain, limit=1)
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
