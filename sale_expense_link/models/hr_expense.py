import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models


class Expense(models.Model):
    _inherit = 'hr.expense'
