import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    sale_order_template_id = fields.Many2one(
        "sale.order.template",
        "Blanket Order Template Reference",
        ondelete="cascade",
        index=True,
    )
    note_header = fields.Html(
        compute="_compute_notes", store=True, string="Header Note"
    )
    note_footer = fields.Html(
        compute="_compute_notes", store=True, string="Footer Note"
    )

    @api.depends("sale_order_template_id")
    def _compute_notes(self):
        for order in self:
            template = order.sale_order_template_id
            if template:
                if not order.note_header or order.note_header == "<p><br></p>":
                    order.note_header = template.note_header
                if not order.note_footer or order.note_footer == "<p><br></p>":
                    order.note_footer = template.note_footer
            else:
                order.note_header = (
                    order.note_header if order.note_header else "<p><br></p>"
                )
                order.note_footer = (
                    order.note_footer if order.note_footer else "<p><br></p>"
                )
