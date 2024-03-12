from datetime import date
from odoo import api, fields, models, _


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    date_confirmed = fields.Date(
        string="Confirmation Date",
        readonly=True,
        index=True,
        copy=False,
        help="Confirmation date of blanket order.",
    )

    def action_confirm(self):
        # Calling super ensures that the original confirmation logic is preserved
        res = super(BlanketOrder, self).action_confirm()
        # Set the confirmation date to today upon confirming the order
        self.write({'date_confirmed': fields.Date.today()})
        return res
