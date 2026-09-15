# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class TimesheetsAnalysisReport(models.Model):
    _inherit = ["timesheets.analysis.report"]

    @api.model
    def _select(self):
        """
        Override to treat timesheets linked to sale order lines with zero price
        as non-billable (no revenue, no billable time).
        """
        select = super()._select()

        # Add the condition OR SOL.price_unit = 0 to both CASE statements
        # to treat zero-price SOLs as non-billable
        # select = select.replace(
        #     "CASE WHEN A.order_id IS NULL THEN 0", "CASE WHEN A.order_id IS NULL OR SOL.price_unit = 0 THEN 0"
        # )
        select = select.replace(
            "WHEN A.order_id IS NULL OR T.service_type in ('manual', 'milestones') THEN 0",
            "WHEN A.order_id IS NULL OR T.service_type in ('manual', 'milestones') OR SOL.price_unit = 0 THEN 0",
        )
        select = select.replace(
            "CASE WHEN A.order_id IS NULL THEN 0 ELSE A.unit_amount END AS billable_time",
            "CASE WHEN A.order_id IS NULL OR SOL.price_unit = 0 THEN 0 ELSE A.unit_amount END AS billable_time",
        )

        return select


