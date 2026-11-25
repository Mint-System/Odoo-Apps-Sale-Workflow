import logging

_logger = logging.getLogger(__name__)
from odoo import models


class HrExpense(models.Model):
    _inherit = "hr.expense"

    def action_reset(self):
        """Remove SO lines when the expense is reset."""
        so_lines = self.so_line_ids
        res = super().action_reset()
        so_lines.unlink()
        return res