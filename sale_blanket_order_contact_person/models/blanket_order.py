from odoo import api, fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    partner_sale_id = fields.Many2one(
        "res.partner",
        compute="_compute_partner_sale_id",
        store=True,
        readonly=False,
        states={"draft": [("readonly", False)]},
    )

    @api.depends("partner_id")
    def _compute_partner_sale_id(self):
        for order in self:
            if order.partner_id:
                addr = order.partner_id.address_get(["sale"])
                order.partner_sale_id = addr.get("sale")
            else:
                order.partner_sale_id = False
