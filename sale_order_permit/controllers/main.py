from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http

class WebsiteSaleCustom(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        if category:
            http.request.session['public_category_id'] = category.id
        else:
            http.request.session.pop('public_category_id', None)

        return super().shop(page=page, category=category, search=search, min_price=min_price, max_price=max_price, ppg=ppg, **post)