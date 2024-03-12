from odoo import fields, models, api


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    incoterm = fields.Many2one(
        "account.incoterms",
        help="International Commercial Terms are a series of predefined commercial terms used in international transactions.",
    )
    picking_policy = fields.Selection(
        [("direct", "As soon as possible"), ("one", "When all products are ready")],
        required=True,
        readonly=True,
        default="direct",
        states={"draft": [("readonly", False)]},
        help="If you deliver all products at once, the delivery order will be scheduled based on the greatest product lead time. Otherwise, it will be based on the shortest.",
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super().onchange_partner_id()
        if not self.incoterm and self.partner_id.sale_incoterm_id:
            self.incoterm = self.partner_id.sale_incoterm_id
        return res