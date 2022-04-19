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