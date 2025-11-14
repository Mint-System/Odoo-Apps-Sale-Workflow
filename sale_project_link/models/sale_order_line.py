# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = ["sale.order.line"]

    def _timesheet_service_generation(self):
        """
        If project is set do not create projects and/or tasks for so lines with service tracking.
        """
        project_ids = self.filtered(
            lambda sol: sol.is_service and sol.product_id.service_tracking != "no"
        ).order_id.project_id
        if project_ids:
            return False
        return super()._timesheet_service_generation()
