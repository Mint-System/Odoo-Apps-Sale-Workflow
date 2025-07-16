import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_product_pricelist = fields.Many2one(compute="_compute_product_pricelist", store=True)

    def get_sale_order_line_pricelist_domain(self, all_partners):
        domain = super().get_sale_order_line_pricelist_domain(all_partners)
        return domain + [("order_id.stage_category", "=", "progress")]
