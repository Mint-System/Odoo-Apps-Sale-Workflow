# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = ["account.analytic.line"]

    def _compute_timesheet_invoice_type(self):
        """
        If the price of the linked sale order line is zero,
        mark the the timehseet line as non billable.
        """
        res = super()._compute_timesheet_invoice_type()
        for line in self:
            if line.so_line and line.so_line.price_unit == 0:
                line.timesheet_invoice_type = "non_billable"
        return res
