import logging
from odoo import fields, models
from odoo import http

_logger = logging.getLogger(__name__)

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    is_dummy = fields.Boolean(help="Used as a placeholder. Products are hidden until another pricelist is selected.")

    public_category_ids = fields.Many2many("product.public.category", string="Website categories")

    def _get_website_pricelists_domain(self, website):
        domain = super()._get_website_pricelists_domain(website)

        # get selected category from session injected in main controller
        product_category_ids = http.request.session.get('product_public_category_ids')
        _logger.warning(f"product_category_ids: {product_category_ids}")


        if product_category_ids:
            # Filter: pricelist must have at least one of these categories, OR no categories assigned
            domain += [
                '|',
                ('public_category_ids', 'in', product_category_ids),
                ('public_category_ids', '=', False),
            ]

        return domain
