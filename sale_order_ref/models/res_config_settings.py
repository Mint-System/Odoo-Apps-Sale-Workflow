# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # The actual parameter
    sale_order_ref_displayname_template = fields.Char(
        string='Sale Order Display Name Template',
        config_parameter='sale_order_ref.displayname_template',
        default='{name} ({ref})',
    )

    # Live preview field
    sale_order_ref_template_example = fields.Char(
        string='Example',
        compute='_compute_sale_order_ref_template_example',
    )

    @api.constrains('sale_order_ref_displayname_template')
    def _check_template_validity(self):
        if self.sale_order_ref_template_example == 'Invalid Template':
            raise ValidationError("Display name template is invalid.")

    @api.depends('sale_order_ref_displayname_template')
    def _compute_sale_order_ref_template_example(self):
        for rec in self:
            try:
                rec.sale_order_ref_template_example = self.env["sale.order"].display_name_formatted(rec.sale_order_ref_displayname_template, "S00042", "Material for Company")
            except (KeyError, ValueError, AttributeError):
                rec.sale_order_ref_template_example = 'Invalid Template'
