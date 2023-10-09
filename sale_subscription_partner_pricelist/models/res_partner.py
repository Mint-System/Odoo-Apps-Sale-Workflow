import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_product_pricelist = fields.Many2one(
        compute="_compute_product_pricelist", store=False, readonly=True
    )

    def _compute_product_pricelist(self):
        res = super()._compute_product_pricelist()
        for partner in self:
            all_partners = (
                (partner.parent_id + partner.parent_id.child_ids)
                if partner.parent_id
                else (partner + partner.child_ids)
            )

            subscriptions = self.env["sale.order"].search(
                [
                    ("partner_id", "in", all_partners.ids),
                    ("is_subscription", "=", "True"),
                    ("stage_category", "in", ["progress"]),
                ]
            )

            if subscriptions:
                pricelist_line = subscriptions.order_line.filtered(
                    lambda l: l.product_id.pricelist_id
                )[:1]
                if pricelist_line:
                    partner.property_product_pricelist = (
                        pricelist_line.product_id.pricelist_id
                    )
        return res
