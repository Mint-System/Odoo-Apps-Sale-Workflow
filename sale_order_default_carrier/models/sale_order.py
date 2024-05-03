from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def _onchange_carrier_id(self):
        for order in self.filtered(lambda so: not so.carrier_id):
            order.carrier_id = order.partner_id.property_delivery_carrier_id
