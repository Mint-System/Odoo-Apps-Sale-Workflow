from odoo import fields, models


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    note_header = fields.Html(translate=False)
    note_footer = fields.Html(translate=False)
