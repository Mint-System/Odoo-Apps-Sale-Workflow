import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_name = fields.Char()
    domain = fields.Char()
    consuling_partner_id = fields.Char()
    cluster_id = fields.Many2one("kubectl.cluster")
