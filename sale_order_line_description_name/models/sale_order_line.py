from odoo import api, models
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()

        # Replace product display name without name
        if self.product_id:
            self.name = self.name.replace(self.product_id.display_name, self.product_id.name)

        return res
