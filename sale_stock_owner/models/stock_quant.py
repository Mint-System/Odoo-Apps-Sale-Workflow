import logging

from odoo import models, api

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _update_available_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None, in_date=None):
        """
        If adjustment is internal and negative then do not assign owner_id.
        This will ensure that a delivered quantity will balance with the incoming quantity. 
        """
        if location_id.usage == "internal" and quantity < 0:
            owner_id = False
        return super()._update_available_quantity(product_id, location_id, quantity, lot_id, package_id, owner_id, in_date)