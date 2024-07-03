import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Datetime(compute="_compute_commitment_date", store=True)

    @api.depends("customer_lead", "product_id")
    def _compute_commitment_date(self):
        for line in self:
            if line.product_id:
                line.commitment_date = line._expected_date()
            else:
                line.commitment_date = False
