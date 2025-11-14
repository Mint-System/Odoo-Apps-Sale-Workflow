import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Datetime(compute="_compute_commitment_date", store=True)

    @api.depends("order_id.commitment_date")
    def _compute_commitment_date(self):
        for line in self:
            line.commitment_date = line.order_id.commitment_date if line.order_id else False

    def write(self, values):
        """Update commitment and deadline date on moves"""
        result = super().write(values)
        if "commitment_date" in values:
            for line in self:
                if line.commitment_date:
                    date_commitment = fields.Datetime.to_datetime(line.commitment_date)
                    date_move = date_commitment - relativedelta(days=line.company_id.security_lead)
                    line.move_ids.write({"date": date_move, "date_deadline": date_commitment})
        return result
