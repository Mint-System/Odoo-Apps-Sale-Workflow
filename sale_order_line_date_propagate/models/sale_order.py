import logging
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("commitment_date")
    def _onchange_commitment_date(self):
        """Always update commitment_date on sale order lines"""
        result = super(SaleOrder, self)._onchange_commitment_date() or {}
        if "warning" not in result and self.commitment_date:
            result["value"] = {
                "order_line": [
                    (1, line.id, {"commitment_date": self.commitment_date})
                    for line in self.order_line
                ]
            }
        return result

    def action_confirm(self):
        """Update commitent_date on each sale order line move"""
        result = super(SaleOrder, self).action_confirm()
        if result:
            for order_line in self.order_line: #.filtered(lambda l: l.commitment_date):
                for move in order_line.move_ids:
                    move.write({"date": (order_line.commitment_date or fields.Datetime.now()) - relativedelta(days=self.company_id.security_lead)})
        return result
