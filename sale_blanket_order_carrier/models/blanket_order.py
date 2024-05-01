from odoo import fields, models, api


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    carrier_id = fields.Many2one('delivery.carrier', string="Delivery Method", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="Fill this field if you plan to invoice the shipping based on picking.")

    @api.onchange('partner_id')
    def _onchange_carrier_id(self):
        for order in self.filtered(lambda bo: not bo.carrier_id):
            order.carrier_id = order.partner_id.property_delivery_carrier_id
