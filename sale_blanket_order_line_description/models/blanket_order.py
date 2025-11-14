import ast

from odoo import api, fields, models


class BlanketOrderLine(models.Model):
    _inherit = "sale.blanket.order.line"

    name = fields.Text("Description", tracking=True)

    @api.onchange("product_id", "original_uom_qty")
    def onchange_product(self):
        current_name = self.name
        super().onchange_product()

        # Get params
        hide_default_code = ast.literal_eval(
            self.env["ir.config_parameter"].sudo().get_param("sale.blanket.order.line.hide_default_code", "False")
        )
        sale_description_only = ast.literal_eval(
            self.env["ir.config_parameter"].sudo().get_param("sale.blanket.order.line.sale_description_only", "False")
        )
        description_sale = self.product_id.with_context(lang=self.order_id.partner_id.lang).description_sale

        # Apply options
        if hide_default_code:
            self.name = self.product_id.name
        else:
            self.name = self.product_id.display_name
        if description_sale and sale_description_only:
            self.name = description_sale
        elif description_sale:
            self.name += "\n" + description_sale

        # Restore current name
        if current_name:
            self.name = current_name
