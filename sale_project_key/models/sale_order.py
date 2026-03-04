# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    project_key = fields.Char(related="project_id.key", string="Project Key")

    @api.depends("partner_id", "project_key")
    def _compute_display_name(self):
        super()._compute_display_name()
        for so in self.sudo():
            if so.project_key:
                so.display_name = f"[{so.project_key}] - {so.display_name}"
