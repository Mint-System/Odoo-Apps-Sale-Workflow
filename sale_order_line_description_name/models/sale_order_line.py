from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if not self.product_id:
            return res
        if not self.product_id.description_sale:
            self.name = self.product_id.name
        return res
