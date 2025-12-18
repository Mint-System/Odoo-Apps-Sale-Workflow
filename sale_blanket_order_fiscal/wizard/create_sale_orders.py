import logging

from odoo import models

_logger = logging.getLogger(__name__)
import ast


class BlanketOrderWizard(models.TransientModel):
    _inherit = "sale.blanket.order.wizard"

    def _prepare_so_vals(self, *kwargs):
        res = super()._prepare_so_vals(*kwargs)
        copy_fiscal = ast.literal_eval(
            self.env["ir.config_parameter"].sudo().get_param("sale_blanket_order_fiscal.copy_fiscal", "False")
        )
        if copy_fiscal:
            res.update(
                {
                    "fiscal_position_id": self.blanket_order_id.fiscal_position_id.id,
                }
            )
        return res
