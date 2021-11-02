from odoo import fields, models, _, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def set_position(self):
        for order in self:
            position = 0
            for line in order.order_line.filtered(lambda l: not l.display_type):
                position += 1
                line.position = position

    # Set position on create
    @api.model
    def create(self, values):
        res = super().create(values)
        res.set_position()

        return res

    # Set position on update
    def write(self, values):
        res = super().write(values)
        self.set_position()

        return res

    def get_position(self, product_id, product_uom_qty):
        self.ensure_one()
        if product_uom_qty:
            lines = self.order_line.filtered(lambda l: l.product_id == product_id and l.product_uom_qty == product_uom_qty)
        else:
            lines = self.order_line.filtered(lambda l: l.product_id == product_id )
        for line in lines:
            return line.position

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    position = fields.Integer("Pos", readonly=True)
