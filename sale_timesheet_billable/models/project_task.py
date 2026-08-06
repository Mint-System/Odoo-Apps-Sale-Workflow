# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    billable = fields.Boolean(default=True)

    @api.constrains("billable", "sale_line_id")
    def _check_sale_line_id_billable(self):
        for record in self:
            if not record.so_line:
                continue

            if record.billable and not record.sale_line_id:
                raise ValidationError(_("Task is billable, a sales order item has to be defined."))

            if not record.billable and record.sale_line_id:
                raise ValidationError(_("Task is not billable, no sales order item should be set."))