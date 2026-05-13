# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def _timesheet_domain_get_invoiced_lines(self, sale_line_delivery):
        """
        Fix for odoo/addons/sale_timesheet/models/account_move.py
        Do not relink invoiced timesheet lines linked with reversed invoices.
        """
        return [
            ("so_line", "in", sale_line_delivery.ids),
            ("project_id", "!=", False),
            ("timesheet_invoice_id", "=", False),
        ]
