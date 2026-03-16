import logging

from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):
    # @http.route()
    # def product(self, product, category='', search='', **kwargs):
    #     public_category_ids = product.public_categ_ids.ids
    #     if public_category_ids:
    #         http.request.session['product_public_category_ids'] = public_category_ids
    #     else:
    #         http.request.session.pop('product_public_category_ids', None)

    #     if category:
    #         http.request.session['public_category_id'] = category
    #     else:
    #         http.request.session.pop('public_category_id', None)

    #     return super().product(product, category, search, **kwargs)

    @http.route()
    def product(self, product, category="", search="", **kwargs):
        # Get dummy pricelist (sequence = 0)
        dummy_pricelist = http.request.env["product.pricelist"].search([("sequence", "=", 0)], limit=1)

        # Reset pricelist in session to dummy
        if dummy_pricelist:
            http.request.session["pricelist"] = dummy_pricelist.id

        # Call parent method
        return super().product(product, category, search, **kwargs)
