from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    