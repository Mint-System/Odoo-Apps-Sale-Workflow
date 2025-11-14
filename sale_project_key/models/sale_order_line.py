# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    project_key = fields.Char(related="project_id.key", string="Project Key")
