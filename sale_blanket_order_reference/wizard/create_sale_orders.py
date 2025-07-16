import logging

from odoo import models

_logger = logging.getLogger(__name__)
import ast


class BlanketOrderWizard(models.TransientModel):
    _inherit = "sale.blanket.order.wizard"

    def _prepare_so_vals(self, *kwargs):
        res = super()._prepare_so_vals(*kwargs)
        copy_ref = ast.literal_eval(
            self.env["ir.config_parameter"].sudo().get_param("sale_blanket_order_reference.copy_ref", "False")
        )
        if copy_ref:
            res.update(
                {
                    "client_order_ref": self.blanket_order_id.client_order_ref,
                }
            )
        return res
