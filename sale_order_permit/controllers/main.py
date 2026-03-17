import logging

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):
    @http.route()
    def product(self, product, category="", search="", **kwargs):
        last_product_id = request.session.get('last_viewed_product_id')
        current_product_id = product.id
        
       
        if last_product_id != current_product_id:
            http.request.session["force_dummy_pricelist"] = True
        
        request.session['last_viewed_product_id'] = product.id

        return super().product(product, category, search, **kwargs)





