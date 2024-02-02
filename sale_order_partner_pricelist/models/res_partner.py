import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_product_pricelist = fields.Many2one(
        compute="_compute_product_pricelist", store=True
    )

    def _compute_product_pricelist(self):
        """
        Check sale order lines with pricelist products.
        Set pricelist from first product and otherwhise reset to first pricelist.
        """
        res = super()._compute_product_pricelist()
        for partner in self:

            all_partners = (
                (partner.parent_id + partner.parent_id.child_ids)
                if partner.parent_id
                else (partner + partner.child_ids)
            )

            sale_order_lines = self.env["sale.order.line"].search(
                [
                    ("order_partner_id", "in", all_partners.ids),
                    ("state", "in", ["sale"]),
                ]
            )

            if sale_order_lines:

                pricelist_line = sale_order_lines.filtered(
                    lambda l: l.product_id.pricelist_id
                )[:1]

                if pricelist_line:
                    partner.property_product_pricelist = (
                        pricelist_line.product_id.pricelist_id
                    )

            else:
                partner.property_product_pricelist = self.env[
                    "product.pricelist"
                ].search([], limit=1)

        return res
