import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_membership_id = fields.Many2one(
        "res.partner",
        string="Membership Contact Address",
        compute="_compute_partner_membership_id",
        store=True,
        readonly=False,
        precompute=True,
    )

    @api.depends("partner_id")
    def _compute_partner_membership_id(self):
        for order in self:
            order.partner_membership_id = (
                order.partner_id.address_get(["membership"])["membership"] if order.partner_id else False
            )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    partner_membership_id = fields.Many2one(
        related="order_id.partner_membership_id",
        string="Membership Contact Address",
        store=True,
        index=True,
        precompute=True,
    )
