import logging

from odoo import models

_logger = logging.getLogger(__name__)


class BlanketOrderWizard(models.TransientModel):
    _inherit = "sale.blanket.order.wizard"

    def _prepare_so_vals(self, *kwargs):
        res = super()._prepare_so_vals(*kwargs)
        res.update(
            {
                "tag_ids": self.blanket_order_id.tag_ids,
            }
        )
        return res
