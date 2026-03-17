# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    phase_id = fields.Many2one("project.task.phase", inverse="_inverse_phase_id")

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
