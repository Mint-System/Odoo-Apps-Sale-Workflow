import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, _


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    def reset_expense_sheets(self):
        """Remove so lines when sheet is set to draft."""
        
        so_lines = self.expense_line_ids.so_line_ids
        _logger.warning(so_lines)
        res = super().reset_expense_sheets()
        so_lines.unlink()
        return res