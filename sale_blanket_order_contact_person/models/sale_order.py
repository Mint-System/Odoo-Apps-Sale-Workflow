from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)

        # Copy contact person if blanket order is passed
        if res.blanket_order_id:
            res.partner_contact_id = res.blanket_order_id.partner_contact_id

        return res