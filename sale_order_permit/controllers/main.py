import logging

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http

_logger = logging.getLogger(__name__)

class WebsiteSaleCustom(WebsiteSale):

    @http.route()
    def product(self, product, category='', search='', **kwargs):
        public_category_ids = product.public_categ_ids.ids
        if public_category_ids:
            http.request.session['product_public_category_ids'] = public_category_ids
        else:
            http.request.session.pop('product_public_category_ids', None)
        
        if category:
            http.request.session['public_category_id'] = category
        else:
            http.request.session.pop('public_category_id', None)

        return super().product(product, category, search, **kwargs)