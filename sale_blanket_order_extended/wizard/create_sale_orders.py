from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class BlanketOrderWizard(models.TransientModel):
    _inherit= "sale.blanket.order.wizard"

    def _prepare_so_vals(
        self,
        *kwargs
    ):
        res = super(BlanketOrderWizard, self)._prepare_so_vals(
            *kwargs
        )
        res.update(
            {
                "fiscal_position_id": self.blanket_order_id.fiscal_position_id.id,
                "client_order_ref": self.blanket_order_id.client_order_ref,
            }
        )
        return res