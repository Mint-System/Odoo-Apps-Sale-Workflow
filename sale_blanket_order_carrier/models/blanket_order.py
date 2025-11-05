from odoo import api, fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    carrier_id = fields.Many2one(
        "delivery.carrier",
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        compute="_compute_carrier_id",
        store=True,
    )

    @api.depends("partner_id")
    def _compute_carrier_id(self):
        for order in self:
            if not order.carrier_id:
                order.carrier_id = order.partner_id.property_delivery_carrier_id
