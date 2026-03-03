import logging

_logger = logging.getLogger(__name__)

from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self.env.context.get("website_id"):
                product = self.env["product.product"].browse(vals["product_id"])
                min_qty = product.sale_min_qty
                if min_qty and vals.get("product_uom_qty", 0) < min_qty:
                    vals["product_uom_qty"] = min_qty

        return super().create(vals_list)
