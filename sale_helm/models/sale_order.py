import logging

_logger = logging.getLogger(__name__)
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_name = fields.Char()
    domain = fields.Char()
    consuling_partner_id = fields.Char()
    cluster_id = fields.Many2One("kubectl.cluster")
