import logging

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_name = fields.Char(inverse="_inverse_project_name")
    domain = fields.Char()
    consulting_partner_id = fields.Many2one("res.partner")
    cluster_id = fields.Many2one("kubectl.cluster")
    chart_ids = fields.One2many("helm.chart", compute="_compute_chart_ids")

    def _compute_chart_ids(self):
        for rec in self:
            rec.chart_ids = rec.order_line.product_id.chart_id

    def _inverse_project_name(self):
        """
        Ensure project name is alphanumerical.
        """
        for rec in self:
            if rec.project_name:
                if not rec.project_name.isalnum():
                    raise ValidationError(_("Project name must only contain alphanumeric characters."))

    def action_confirm(self):
        """
        For each order line with chart, install chart.
        """
        res = super().action_confirm()
        for order in self.filtered("chart_ids"):
            namespace_id = self.env["kubectl.namespace"].create(
                {"name": order.project_name, "cluster_id": order.cluster_id}
            )
            for line in order.order_line:
                release_id = line.product_id.chart_id.create_release(namespace_id, order.partner_id)
                release_id.action_install()
                line.release_id = release_id
        return res
