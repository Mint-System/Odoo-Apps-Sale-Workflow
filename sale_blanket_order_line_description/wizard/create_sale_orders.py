import logging

from odoo import models

_logger = logging.getLogger(__name__)


class BlanketOrderWizard(models.TransientModel):
    _inherit = "sale.blanket.order.wizard"

    def _prepare_so_line_vals(self, line):
        res = super()._prepare_so_line_vals(line)
        res.update({"name": line.blanket_line_id.name})
        return res
