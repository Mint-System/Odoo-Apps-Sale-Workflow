import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        Propagate sale order data to linked project.
        """
        res = super().action_confirm()

        for order in self:
            # Write partner to project
            _logger.warning(["WRITE", order.project_id])
            if order.project_id and not order.project_id.partner_id:
                order.project_id.write(
                    {
                        "partner_id": order.partner_id.id,
                    }
                )
            # Write partner to project tasks
            for task in order.project_id.task_ids.filtered(lambda t: not t.partner_id):
                task.write(
                    {
                        "partner_id": order.partner_id.id,
                    }
                )
            # Write analytic account to linked projects
            if order.project_ids:
                order.project_ids.write(
                    {
                        "analytic_account_id": order.analytic_account_id.id,
                    }
                )
        return res
