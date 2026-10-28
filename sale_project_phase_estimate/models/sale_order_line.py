# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    estimate_ids = fields.One2many("project.estimate", "sale_line_id")

    def _timesheet_create_task_prepare_values(self, project):
        values = super()._timesheet_create_task_prepare_values(project)
        if self.estimate_ids:
            values["phase_id"] = self.estimate_ids[0].phase_id.id
        return values

    def _timesheet_service_generation(self):
        order_project_ids = {line.id: line.order_id.project_id.id for line in self}
        super()._timesheet_service_generation()
        for line in self:
            if line.project_id and line.estimate_ids:
                if not order_project_ids.get(line.id):
                    line.estimate_ids.project_id = line.project_id
