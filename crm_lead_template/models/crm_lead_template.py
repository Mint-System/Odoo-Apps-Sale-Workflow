# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CRMLeadTemplate(models.Model):
    _name = "crm.lead.template"
    _description = "CRM Lead Template"

    name = fields.Char()
    description = fields.Html("Notes")
    tag_ids = fields.Many2many(
        "crm.tag",
        "crm_template_tag_rel",
        "lead_template_id",
        "tag_id",
        string="Tags",
        help="Classify and analyze your lead/opportunity categories like: Training, Service",
    )
