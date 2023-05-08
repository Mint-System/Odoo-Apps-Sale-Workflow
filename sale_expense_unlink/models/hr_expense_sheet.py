import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, _


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    def action_unpost(self):
        """Remove so lines when sheet is cancelled."""
        
        so_lines = self.expense_line_ids.so_line_ids
        res = super().action_unpost()
        so_lines.unlink()
        return res