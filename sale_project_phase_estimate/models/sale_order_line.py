# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    estimate_ids = fields.One2many("project.estimate", "sale_line_id")

    def _timesheet_service_generation(self):
        super()._timesheet_service_generation()
        for line in self:
            if line.project_id and line.estimate_ids:
                line.estimate_ids.project_id = line.project_id
