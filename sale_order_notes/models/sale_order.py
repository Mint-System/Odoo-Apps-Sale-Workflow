import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    note_header = fields.Html(translate=False)
    note_footer = fields.Html(translate=False)
