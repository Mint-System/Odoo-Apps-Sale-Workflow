# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools.misc import unquote

_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def _domain_so_line(self):
        """
        Overwrite domain defined in odoo/addons/sale_timesheet/models/account.py
        """
        domain = expression.AND(
            [
                self.env["sale.order.line"]._sellable_lines_domain(),
                [
                    ("qty_delivered_method", "in", ["analytic", "timesheet"]),
                    ("is_service", "=", True),
                    ("is_expense", "=", False),
                    ("state", "=", "sale"),
                    ("order_partner_id.commercial_partner_id", "=", unquote("commercial_partner_id")),
                ],
            ]
        )

        # Add condition order_id must match task_order_id
        order_id_condition = [("order_id", "=", unquote("task_order_id"))]

        final_domain = expression.AND(
            [
                domain,
                order_id_condition,
            ]
        )

        return str(final_domain)

    billable = fields.Boolean(related="task_id.billable")
    task_order_id = fields.Many2one(related="task_id.sale_order_id")
    so_line = fields.Many2one(compute="_compute_so_line", store=True, readonly=False, domain=_domain_so_line)

    @api.constrains("so_line", "billable")
    def _check_so_line_price_unit(self):
        for record in self:
            if not record.so_line:
                continue

            if record.billable and record.so_line.price_unit <= 0:
                raise ValidationError(_("Task is billable, only order lines with a price > 0.0 are valid."))

            if not record.billable and record.so_line.price_unit != 0:
                raise ValidationError(_("Task is not billable, only order lines price 0.0 are valid."))
