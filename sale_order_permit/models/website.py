import logging
from odoo.http import request
from odoo import models

_logger = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = 'website'

    # def _get_current_pricelist(self):
    #     pricelist = super()._get_current_pricelist()

    #     # domain filtered = category matching
    #     available_pricelists = self.get_pricelist_available()

    #     # If pricelist is not in filtered list, fall back to first available
    #     if pricelist and pricelist not in available_pricelists:
    #         if available_pricelists:
    #             pricelist = available_pricelists[0]
    #             # Update session to persist selection
    #             if hasattr(self.env, 'request') and self.env.request.session:
    #                 self.env.request.session['website_sale_current_pl'] = pricelist.id
    #             _logger.info("Fallback: current pricelist %s not in filtered list, using %s", pricelist.id, available_pricelists[0].id)

    #     return pricelist

    # def _compute_pricelist_id(self):
    #     for website in self:
    #         # Get actual current pricelist (via _get_current_pricelist)
    #         pricelist = website._get_current_pricelist()
    #         _logger.warning(f"pricelist: {pricelist}")
    #         _logger.warning(f"request.session.get('website_sale_current_pl'): {request.session.get('website_sale_current_pl')}")


    #         # If no pricelist is explicitly selected (session empty), return False for UI
    #         if not request.session.get('website_sale_current_pl'):
    #             website.pricelist_id = False  # Show "Select Price List"
    #         else:
    #             website.pricelist_id = pricelist  # Show actual pricelist name