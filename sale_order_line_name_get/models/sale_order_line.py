from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def name_get(self):
        """OVERWRITE Return display name with product name"""
        result = []
        for so_line in self.sudo():
            name = "%s - %s / %s" % (
                so_line.order_id.name,
                so_line.product_id.name,
                so_line.name and so_line.name.split("\n")[0],
            )
            if so_line.order_partner_id.ref:
                name = "%s (%s)" % (name, so_line.order_partner_id.ref)
            result.append((so_line.id, name))
        return result
