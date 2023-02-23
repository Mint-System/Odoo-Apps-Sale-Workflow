from odoo import api, models
import ast


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        prefix_sale_description = ast.literal_eval(self.env["ir.config_parameter"].sudo().get_param("sale_order_line_description_name.prefix_sale_description", "False"))

        # Set product name without reference as description
        if not self.product_id.description_sale:
            self.name = self.product_id.name

        # Prefix description with product name
        if self.product_id.description_sale and prefix_sale_description:
            self.name = self.product_id.name + '\n' + self.name

        return res
