from odoo import api, fields, models, _


class BlanketOrderLine(models.Model):
    _inherit = "sale.blanket.order.line"

    name = fields.Text("Description", tracking=True)

    @api.onchange("product_id", "original_uom_qty")
    def onchange_product(self):
        current_name = self.name
        super().onchange_product()
        if self.product_id.description_sale:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
            )
            self.name = product.description_sale
        elif self.product_id:
            self.name = self.product_id.name
        if current_name:
            self.name = current_name
