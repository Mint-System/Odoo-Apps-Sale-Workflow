from odoo import api, fields, models, _


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    tag_ids = fields.Many2many('crm.tag', 'sale_blanket_order_tag_rel', 'order_id', 'tag_id', string='Tags')