import logging

_logger = logging.getLogger(__name__)

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_uom_qty = fields.Float(
        inverse="_inverse_product_uom_qty",
    )

    def _inverse_product_uom_qty(self):
        for rec in self:
            product = rec.product_id.product_tmpl_id
            if product and product.is_sale_own_min_qty_set and product.sale_min_qty > rec.product_uom_qty:
                rec.product_uom_qty = product.sale_min_qty
