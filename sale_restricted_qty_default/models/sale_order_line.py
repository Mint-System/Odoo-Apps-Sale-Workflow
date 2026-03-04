import logging

_logger = logging.getLogger(__name__)

from odoo import models, api, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_uom_qty = fields.Float(
        string="Quantity",
        compute='_compute_product_uom_qty',
        inverse='_inverse_product_uom_qty',
        digits='Product Unit of Measure', default=1.0,
        store=True, readonly=False, required=True, precompute=True)


    def _inverse_product_uom_qty(self):
        for rec in self:
            product = rec.product_id
            if product and product.sale_min_qty and product.sale_min_qty > self.product_uom_qty:
                self.product_uom_qty = product.sale_min_qty


