from odoo import fields, models, _, api
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_prices(self):
        super().update_prices()
        for line in self.order_line:
            line._onchange_price_rule()

    @api.onchange('commitment_date')
    def _onchange_commitment_date(self):
        super()._onchange_commitment_date()
        for line in self.order_line:
            line._onchange_price_rule()
