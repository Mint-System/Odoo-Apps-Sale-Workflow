import logging
from odoo import models

_logger = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = 'website'

    def _get_current_pricelist(self):
            pricelist = super()._get_current_pricelist()

            # domain filtered = category matching
            available_pricelists = self.get_pricelist_available()

            # If pricelist is not in filtered list, fall back to first available
            if pricelist and pricelist not in available_pricelists:
                if available_pricelists:
                    pricelist = available_pricelists[0]
                    # Update session to persist selection
                    if hasattr(self.env, 'request') and self.env.request.session:
                        self.env.request.session['website_sale_current_pl'] = pricelist.id
                    _logger.info("Fallback: current pricelist %s not in filtered list, using %s", pricelist.id, available_pricelists[0].id)

            return pricelist