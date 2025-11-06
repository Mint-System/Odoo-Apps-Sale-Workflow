from odoo import fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    comment = fields.Text(tracking=True)
