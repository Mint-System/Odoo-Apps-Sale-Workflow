from odoo import fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    carrier_id = fields.Many2one('delivery.carrier', string="Delivery Method", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="Fill this field if you plan to invoice the shipping based on picking.")