import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    note_header = fields.Html(compute="_compute_notes", store=True, readonly=False)
    note_footer = fields.Html(compute="_compute_notes", store=True, readonly=False)

    @api.depends("sale_order_template_id")
    def _compute_notes(self):
        for order in self:
            if order.sale_order_template_id:
                order.note_header = order.sale_order_template_id.note_header
                order.note_footer = order.sale_order_template_id.note_footer
            else:
                order.note_header = False
                order.note_footer = False
