# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    # Make project field editable
    project_id = fields.Many2one('project.project', readonly=False, states={})