from odoo import fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    note_header = fields.Html(translate=False)
    note_footer = fields.Html(translate=False)
