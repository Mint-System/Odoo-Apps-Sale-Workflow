from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_invoiceable_lines(self, final=False):
        """Filter lines with non billable products."""
        invoiceable_lines = super()._get_invoiceable_lines(final=final)
        return invoiceable_lines.filtered(lambda l: l.product_id.billable)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('qty_invoiced', 'qty_delivered', 'product_uom_qty', 'order_id.state')
    def _get_to_invoice_qty(self):
        super()._get_to_invoice_qty()
        for line in self:
            if not line.product_id.billable:
                line.qty_to_invoice = 0

    @api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity', 'product_uom_qty')
    def _get_invoice_qty(self):
        super()._get_invoice_qty()
        for line in self:
            if not line.product_id.billable:
                line.qty_invoiced = line.product_uom_qty