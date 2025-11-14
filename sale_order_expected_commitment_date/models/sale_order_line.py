import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("customer_lead", "product_id")
    def _onchange_customer_lead_set_commitment_date(self):
        _logger.warning(["SET COMMITMENT DATE", self._expected_date()])
        if self.product_id:
            self.write({"commitment_date": self._expected_date()})
