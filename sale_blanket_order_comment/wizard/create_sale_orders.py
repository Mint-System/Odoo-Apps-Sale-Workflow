import logging

from odoo import models

_logger = logging.getLogger(__name__)
import ast


class BlanketOrderWizard(models.TransientModel):
    _inherit = "sale.blanket.order.wizard"

    def _prepare_so_vals(self, *kwargs):
        res = super()._prepare_so_vals(*kwargs)
        copy_comment = ast.literal_eval(
            self.env["ir.config_parameter"].sudo().get_param("sale_blanket_order_comment.copy_comment", "False")
        )
        if copy_comment:
            res.update(
                {
                    "comment": self.blanket_order_id.comment,
                }
            )
        return res
