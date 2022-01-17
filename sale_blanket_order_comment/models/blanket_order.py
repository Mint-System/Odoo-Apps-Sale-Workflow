from xml.etree.ElementTree import Comment
from odoo import api, fields, models, _


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    comment = fields.Text(tracking=True)
