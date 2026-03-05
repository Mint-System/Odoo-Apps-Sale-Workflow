# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CRMLead(models.Model):
    _inherit = "crm.lead"

    template_id = fields.Many2one(
        comodel_name="crm.lead.template",
        string="Lead Template",
        inverse="_inverse_template_id",
        store=True,
        readonly=False,
    )

    def _inverse_template_id(self):
        """
        Update templated fiels if they are empty and template is updated.
        """
        for lead in self:
            if not lead.description:
                lead.description = lead.template_id.description
            if not lead.tag_ids:
                lead.tag_ids = lead.template_id.tag_ids
