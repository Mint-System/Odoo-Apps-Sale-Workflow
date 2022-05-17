from odoo import fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    partner_contact_id = fields.Many2one('res.partner', string="Contact Person", states={"draft": [("readonly", False)]})
