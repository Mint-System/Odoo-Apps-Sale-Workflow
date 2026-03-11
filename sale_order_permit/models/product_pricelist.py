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

        # get category from session injected in main controller
        public_category_id = http.request.session.get('public_category_id')
        _logger.warning(f"context: {self.env.context}")


        if public_category_id:
            # TODO: add parents?

            # Extend domain: pricelist must have provided category or no categories 
            domain += [
                '|',
                ('public_category_ids', 'in', [public_category_id]),
                ('public_category_ids', '=', False),
            ]

        return domain
