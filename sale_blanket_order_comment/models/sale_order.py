from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)
import ast


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        sale_ordrer = super(SaleOrder, self).create(vals)
        copy_comment = ast.literal_eval(self.env['ir.config_parameter'].sudo().get_param('sale_blanket_order_comment.copy_comment', 'False'))
        if sale_order.blanket_order_id and copy_comment:
            sale_order.comment = sale_order.blanket_order_id.comment
        return sale_order