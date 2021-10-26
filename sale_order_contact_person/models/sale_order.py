from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_contact_id = fields.Many2one('res.partner', string="Contact Person")
    partner_contact_shipping_id = fields.Many2one('res.partner', string="Contact Person (Delivery)")
