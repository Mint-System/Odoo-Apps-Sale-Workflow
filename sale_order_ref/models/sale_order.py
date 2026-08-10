# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ref = fields.Char("Reference", copy=False)

    @api.model
    def display_name_formatted(self, display_name_template, name, ref):
        return display_name_template.format(name=name, ref=ref)

    @api.depends("ref")
    def _compute_display_name(self):
        display_name_template = self.env['ir.config_parameter'].sudo().get_param('sale_order_ref.displayname_template', default=False)
        
        super()._compute_display_name()
        for rec in self:
            if display_name_template and rec.ref and rec.name:
                rec.display_name = self.display_name_formatted(display_name_template, rec.name, rec.ref)
