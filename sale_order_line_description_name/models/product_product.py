from odoo import models

class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_display_name(self):
        super()._compute_display_name()
        if self.env.context.get("from_sale_line"):
            for product in self:
                # show only the template name
                product.product_tmpl_id.display_name = product.product_tmpl_id.name