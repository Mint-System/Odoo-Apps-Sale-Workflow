from odoo import api, fields, models, _


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    state = fields.Selection(selection_add=[('cancel', 'Cancel')])

    def action_cancel(self):
        res = super().action_cancel()
        for order in self:
            order.write({"state": "cancel"})
        return res