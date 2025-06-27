import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    chart_ids = fields.One2many("helm.chart", compute="_compute_chart_ids")
    project_name = fields.Char()
    domain = fields.Char()
    consulting_partner_id = fields.Many2one("res.partner")
    cluster_id = fields.Many2one("kubectl.cluster")

    def _compute_chart_ids(self):
        for rec in self:
            rec.chart_ids = rec.order_line.product_id.chart_ids
