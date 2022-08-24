from odoo import api, fields, models, _
import ast


class BlanketOrderLine(models.Model):
    _inherit = "sale.blanket.order.line"

    name = fields.Text("Description", tracking=True)

    @api.onchange("product_id", "original_uom_qty")
    def onchange_product(self):
        current_name = self.name
        super().onchange_product()
        hide_default_code = ast.literal_eval(self.env["ir.config_parameter"].sudo().get_param("sale.blanket.order.line.hide_default_code", "False"))
        # Set default name
        self.name = self.product_id.get_product_multiline_description_sale()
        # If sale description is set, show sale description only
        if self.product_id.description_sale:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
            )
            self.name = product.description_sale
        # Otherwise remove default code if param is set 
        elif hide_default_code:
            self.name = self.product_id.name
        # Restore current name
        if current_name:
            self.name = current_name
