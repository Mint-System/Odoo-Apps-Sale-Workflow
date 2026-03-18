import logging

from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):
    @http.route()
    def product(self, product, category="", search="", **kwargs):
        res = super().product(product, category, search, **kwargs)
        last_product_id = http.request.session.get('last_viewed_product_id')
        current_product_id = product.id

        for key, value in http.request.session.items():
            _logger.warning(f"##### {key}: {value}")

        _logger.warning(f"##### current_product_id: {current_product_id}")
        
       
        if last_product_id != current_product_id:
            http.request.session["force_dummy_pricelist"] = True
            dummy_pricelist = http.request.env['product.pricelist'].sudo().search(
                [('sequence', '=', 0)],
                limit=1
            )
            if "website_sale_current_pl" in  http.request.session:
                http.request.session["website_sale_current_pl"] = dummy_pricelist.id
            if "website_sale_selected_pl_id" in  http.request.session:
                http.request.session["website_sale_selected_pl_id"] = dummy_pricelist.id
            if "chosen_pricelist_id" in http.request.session:
                http.request.session["chosen_pricelist_id"] = dummy_pricelist.id
        
        http.request.session['last_viewed_product_id'] = product.id

        return res





