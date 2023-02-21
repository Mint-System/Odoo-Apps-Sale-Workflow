from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    repeat_sale_line_position = fields.Boolean()