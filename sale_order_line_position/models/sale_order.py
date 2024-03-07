import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def set_position(self):
        for order in self:
            position = 0
            for line in order.order_line.filtered(lambda l: not l.display_type):
                if line.product_id.repeat_sale_line_position:
                    position += 0
                else:
                    position += 1
                line.position = position

    @api.model
    def create(self, values):
        res = super().create(values)
        res.set_position()
        return res

    def write(self, values):
        res = super().write(values)
        self.set_position()
        return res

    def get_position(self, product_id, product_uom_qty=False):
        self.ensure_one()
        if product_uom_qty:
            lines = self.order_line.filtered(
                lambda l: l.product_id == product_id
                and l.product_uom_qty == product_uom_qty
            )
        else:
            lines = self.order_line.filtered(lambda l: l.product_id == product_id)
        for line in lines:
            return line.position
        return 0


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    position = fields.Char("Pos", readonly=True)
