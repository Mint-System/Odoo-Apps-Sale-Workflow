import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    orig_price_unit = fields.Float("Original Price")
    temp_price_unit = fields.Float("Temporary Price", inverse="_inverse_temp_price_unit")

    def _inverse_temp_price_unit(self):
        """
        Set product price to temporary price and store orig price.
        """
        for line in self:
            if line.temp_price_unit > 0.0:
                line.orig_price_unit = line.price_unit
                line.price_unit = line.temp_price_unit

    def _compute_invoice_status(self):
        """
        Reset product price to original price if line is invoiced.
        """
        res = super()._compute_invoice_status()
        for line in self:
            if line.temp_price_unit > 0.0 and line.invoice_status == "invoiced":
                line.price_unit = line.orig_price_unit
                line.temp_price_unit = 0.0
                line.order_id.message_post(
                    body=_("Resetted temporary price and restored original price."),
                    type="notification",
                )
        return res
