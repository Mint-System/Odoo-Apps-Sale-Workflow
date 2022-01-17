from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    comment = fields.Text(tracking=True)

    @api.model
    def create(self, vals):
        sale_order = super(SaleOrder, self).create(vals)

        if sale_order.blanket_order_id:
            sale_order.comment = sale_order.blanket_order_id.comment

        return sale_order