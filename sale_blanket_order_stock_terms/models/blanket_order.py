from odoo import api, fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    incoterm = fields.Many2one(
        "account.incoterms",
        help="International Commercial Terms are a series of predefined commercial terms used in international transactions.",
        compute="_compute_incoterm",
        store=True,
    )
    picking_policy = fields.Selection(
        [("direct", "As soon as possible"), ("one", "When all products are ready")],
        required=True,
        readonly=True,
        default="direct",
        states={"draft": [("readonly", False)]},
        help="If you deliver all products at once, the delivery order will be scheduled based on the greatest product lead time. Otherwise, it will be based on the shortest.",
    )

    @api.depends("partner_id")
    def _compute_incoterm(self):
        for order in self:
            if order.partner_id.sale_incoterm_id:
                order.incoterm = order.partner_id.sale_incoterm_id
            else:
                order.incoterm = False
