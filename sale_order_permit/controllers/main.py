import logging

from odoo import http

from odoo.http import request

from odoo.addons.web.controllers.home import Home
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(WebsiteSale):
    @http.route()
    def product(self, product, category="", search="", **kwargs):
        res = super().product(product, category, search, **kwargs)
        last_product_id = http.request.session.get("last_viewed_product_id")
        current_product_id = product.id

        if last_product_id != current_product_id:
            http.request.session["force_dummy_pricelist"] = True
            dummy_pricelist = http.request.env["product.pricelist"].sudo().search([("sequence", "=", 0)], limit=1)
            if "website_sale_current_pl" in http.request.session:
                http.request.session["website_sale_current_pl"] = dummy_pricelist.id
            if "website_sale_selected_pl_id" in http.request.session:
                http.request.session["website_sale_selected_pl_id"] = dummy_pricelist.id
            if "chosen_pricelist_id" in http.request.session:
                http.request.session["chosen_pricelist_id"] = dummy_pricelist.id

        http.request.session["last_viewed_product_id"] = product.id

        return res

class ClearCartOnLogin(Home):
    @http.route()
    def web_login(self, redirect=None, **kw):
        # Remember the state *before* login
        pre_sale_order_id = request.session.get('sale_order_id')

        # Let Odoo perform the normal login flow
        response = super(ClearCartOnLogin, self).web_login(redirect=redirect, **kw)

        # Discard the anonymous cart that was stored in the session
        if pre_sale_order_id:
            order = request.env['sale.order'].sudo().browse(pre_sale_order_id)
            # Unlink only if it is still a draft and actually came from the website
            if order.exists() and order.state == 'draft' and order.website_id:
                order.unlink()

        # Remove any existing webshop draft orders for the logged-in user
        SaleOrder = request.env['sale.order'].sudo()
        existing_carts = SaleOrder.search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('state', '=', 'draft'),
            ('website_id', '!=', False),
        ])
        if existing_carts:
            existing_carts.unlink()

        # Make sure the session no longer references a cart
        request.session.pop('sale_order_id', None)

        return response