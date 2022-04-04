from odoo import api, fields, models, _

class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    note_header = fields.Html()
    note_footer = fields.Html()
