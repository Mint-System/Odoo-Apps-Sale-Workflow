from odoo import fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    tag_ids = fields.Many2many(
        comodel_name="crm.tag",
        relation="sale_blanket_order_tag_rel",
        column1="order_id",
        column2="tag_id",
        string="Tags",
    )
