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
        quantity=False,
        reserved_quantity=False,
        lot_id=None,
        package_id=None,
        owner_id=None,
        in_date=None,
    ):
        """
        If adjustment is internal do not assign owner_id.
        This will ensure that a delivered quantity will balance with the incoming quantity.
        """
        ctx = dict(self.env.context)

        if location_id.usage == "internal":
            if "quants_cache" in ctx:
                ctx.pop("quants_cache")
            owner_id = None
            return super(StockQuant, self.with_context(ctx))._update_available_quantity(
                product_id, location_id, quantity, reserved_quantity, lot_id, package_id, owner_id, in_date
            )
        else:
            return super()._update_available_quantity(
                product_id,
                location_id,
                quantity,
                reserved_quantity,
                lot_id,
                package_id,
                owner_id,
                in_date,
            )
