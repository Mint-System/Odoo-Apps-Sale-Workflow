from odoo import models, fields

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    is_dummy = fields.Boolean(
        help="Used as a placeholder. Products are hidden until another pricelist is selected."
    )


