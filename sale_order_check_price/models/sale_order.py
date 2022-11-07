from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            lines_without_price = order.order_line.filtered(lambda l: l.price_unit == 0.0 and l.product_id != order.carrier_id.product_id)
            if lines_without_price:
                raise UserError(_('The order %s has lines with a price of zero. Set a price before confirming the order.') % order.name)
        return super().action_confirm()
