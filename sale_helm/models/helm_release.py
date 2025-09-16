import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HelmRelease(models.Model):
    _inherit = "helm.release"

    sale_line_ids = fields.One2many("sale.order.line", "release_id")

    def _get_eval_context(self):
        """
        This eval context can be accessed by the value python expressions.
        """
        res = super()._get_eval_context()
        res["order_id"] = self.sale_line_ids[0].order_id if self.sale_line_ids else False
        return res
