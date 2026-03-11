import logging

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http

_logger = logging.getLogger(__name__)

class WebsiteSaleCustom(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        # here category is category object
        if category:
            http.request.session['public_category_id'] = category.id
        else:
            http.request.session.pop('public_category_id', None)

        return super().shop(page=page, category=category, search=search, min_price=min_price, max_price=max_price, ppg=ppg, **post)


    @http.route()
    def product(self, product, category='', search='', **kwargs):
        # here category is category id
        if category:
            http.request.session['public_category_id'] = category
        else:
            http.request.session.pop('public_category_id', None)

        return super().product(product, category, search, **kwargs)