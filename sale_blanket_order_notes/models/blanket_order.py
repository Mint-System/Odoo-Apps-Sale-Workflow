from odoo import api, fields, models, _

class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    note_header = fields.Html()
    note_footer = fields.Html()
