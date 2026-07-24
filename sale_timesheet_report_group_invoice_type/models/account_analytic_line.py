# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def get_task_name(self):
        """
        Returns the name of task_id or helpdesk_ticket_id if available.
        Handles missing fields safely.
        """
        self.ensure_one()

        # Check task_id
        if hasattr(self, "task_id") and self.task_id:
            return self.task_id.name

        # Check helpdesk_ticket_id
        if hasattr(self, "helpdesk_ticket_id") and self.helpdesk_ticket_id:
            return self.helpdesk_ticket_id.name

        return False
