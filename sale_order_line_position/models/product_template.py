from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    repeat_sale_line_position = fields.Boolean()
