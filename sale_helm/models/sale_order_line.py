import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    release_id = fields.Many2one("helm.release")

    def _install_chart(self, namespace_id):
        """
        Create and install chart release.
        """
        self.ensure_one()
        chart_id = self.product_id.chart_id
        release_id = self.release_id.create(
            {
                "name": self.order_id.project_name,
                "chart_id": chart_id.id,
                "context_id": self.order_id.cluster_id.context_ids[0].id,
                "namespace_id": namespace_id.id,
                "partner_id": self.order_partner_id.id,
            }
        )
