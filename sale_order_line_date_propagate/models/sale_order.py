import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("commitment_date")
    def _compute_order_line_commitment_date(self):
        """Always update commitment_date on sale order lines"""
        for order in self:
            if order.commitment_date:
                for line in order.order_line:
                    line.commitment_date = order.commitment_date

    def action_confirm(self):
        """Update commitment_date on each sale order line move"""
        result = super().action_confirm()
        if result:
            for order_line in self.order_line:
                for move in order_line.move_ids:
                    move.write(
                        {
                            "date": (order_line.commitment_date or fields.Datetime.now())
                            - relativedelta(days=self.company_id.security_lead)
                        }
                    )
        return result
