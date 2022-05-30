from odoo import api, fields, models, _


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    note_header = fields.Html(translate=False)
    note_footer = fields.Html(translate=False)
