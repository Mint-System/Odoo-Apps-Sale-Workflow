from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    note_header = fields.Html(translate=True)
    note_footer = fields.Html(translate=True)
