from odoo import fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    date_confirmed = fields.Date(
        readonly=True,
        index=True,
        copy=False,
    )

    def action_confirm(self):
        # Calling super ensures that the original confirmation logic is preserved
        res = super(BlanketOrder, self).action_confirm()
        # Set the confirmation date to today upon confirming the order
        self.write({"date_confirmed": fields.Date.today()})
        return res
