import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    orig_price_unit = fields.Float("Original Price")
    temp_price_unit = fields.Float("Temporary Price")

    @api.depends("temp_price_unit")
    def _compute_price_unit(self):
        """
        Set product price to temporary price if line is invoiced.
        """
        super()._compute_price_unit()
        for line in self:
            if line.temp_price_unit > 0.0:
                line.orig_price_unit = line.price_unit
                line.price_unit = line.temp_price_unit

    def _compute_invoice_status(self):
        """
        Reset product price to original price if line is invoiced.
        """
        res = super()._compute_invoice_status()
        _logger.warning(["_compute_invoice_status", self])
        for line in self:
            _logger.warning([line.temp_price_unit, line.invoice_status])
            if line.temp_price_unit > 0.0 and line.invoice_status == "invoiced":
                line.price_unit = line.orig_price_unit
                line.temp_price_unit = 0.0
                line.order_id.message_post(
                    body=_("Resetted temporary price and restored original price."),
                    type="notification",
                )
        return res
