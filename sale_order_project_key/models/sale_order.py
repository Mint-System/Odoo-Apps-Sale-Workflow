import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        """Propagate sale order data to linked project."""

        res = super()._action_confirm()
        # Write partner to project
        if self.project_id and not self.project_id.partner_id:
            self.project_id.write(
                {
                    "partner_id": self.partner_id.id,
                }
            )
        # Write partner to project tasks
        for task in self.project_id.task_ids.filtered(lambda t: not t.partner_id):
            task.write(
                {
                    "partner_id": self.partner_id.id,
                }
            )
        # Write analytic account to linked projects
        if self.project_ids:
            self.project_ids.write(
                {
                    "analytic_account_id": self.analytic_account_id.id,
                }
            )
        return res
