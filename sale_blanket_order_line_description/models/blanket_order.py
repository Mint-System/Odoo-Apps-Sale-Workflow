from odoo import api, fields, models, _


class BlanketOrderLine(models.Model):
    _inherit = "sale.blanket.order.line"

    @api.onchange("product_id")
    def product_id_change(self):
        if self.product_id.description_sale:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
            )
            self.name = product.description_sale
        elif self.product_id:
            self.name = self.product_id.name
