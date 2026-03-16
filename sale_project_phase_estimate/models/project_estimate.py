# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProjectEstimate(models.Model):
    _inherit = "project.estimate"

    sale_line_id = fields.Many2one("sale.order.line")
    partner_id = fields.Many2one("res.partner", related="project_id.partner_id")
