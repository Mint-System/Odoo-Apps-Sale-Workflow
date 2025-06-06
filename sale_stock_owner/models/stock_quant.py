import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _update_available_quantity(
        self,
        product_id,
        location_id,
        quantity,
        lot_id=None,
        package_id=None,
        owner_id=None,
        in_date=None,
    ):
        if location_id.clear_owner:
            owner_id = False

        return super()._update_available_quantity(
            product_id, location_id, quantity, lot_id, package_id, owner_id, in_date
        )