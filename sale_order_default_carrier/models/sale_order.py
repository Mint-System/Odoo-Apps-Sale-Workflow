import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    carrier_id = fields.Many2one(
        "delivery.carrier",
        string="Delivery Method",
        compute="_compute_carrier_id",
        store=True,
    )

    @api.depends("partner_id")
    def _compute_carrier_id(self):
        for order in self:
            if not order.carrier_id:
                order.carrier_id = order.partner_id.property_delivery_carrier_id
