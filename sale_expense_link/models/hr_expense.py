import logging

_logger = logging.getLogger(__name__)
from odoo import _, api, fields, models


class HrExpense(models.Model):
    _inherit = "hr.expense"

    account_move_line_ids = fields.One2many("account.move.line", "expense_id")
    so_line_ids = fields.One2many("sale.order.line", compute="_compute_so_line_ids")

    @api.depends("account_move_line_ids")
    def _compute_so_line_ids(self):
        for rec in self:
            so_line_ids = rec.mapped("account_move_line_ids.analytic_line_ids.so_line")
            rec.so_line_ids = so_line_ids


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    def action_open_so_lines(self):
        self.ensure_one()
        return {
            "name": _("Sale Order Lines"),
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "sale.order.line",
            "domain": [("id", "in", self.expense_line_ids.so_line_ids.ids)],
        }
