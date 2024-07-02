import ast

from odoo import api, fields, models


class BlanketOrderLine(models.Model):
    _inherit = "sale.blanket.order.line"

    name = fields.Text(
        "Description", tracking=True, compute="_compute_name", store=True, readonly=False,
    )

    @api.depends("product_id", "original_uom_qty")
    def _compute_name(self):
        for line in self:
            current_name = line.name

            # Get params
            hide_default_code = ast.literal_eval(
                line.env["ir.config_parameter"]
                .sudo()
                .get_param("sale.blanket.order.line.hide_default_code", "False")
            )
            sale_description_only = ast.literal_eval(
                line.env["ir.config_parameter"]
                .sudo()
                .get_param("sale.blanket.order.line.sale_description_only", "False")
            )
            description_sale = line.product_id.with_context(
                lang=line.order_id.partner_id.lang
            ).description_sale

            # Apply options
            if hide_default_code:
                line.name = line.product_id.name
            else:
                line.name = line.product_id.display_name

            if description_sale and sale_description_only:
                line.name = description_sale
            elif description_sale:
                line.name += "\n" + description_sale

            # Restore current name
            if current_name:
                line.name = current_name
