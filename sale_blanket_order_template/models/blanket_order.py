import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    sale_order_template_id = fields.Many2one(
        "sale.order.template",
        ondelete="cascade",
        index=True,
        inverse="_inverse_sale_order_template_id",
        store=True,
    )

    def _inverse_sale_order_template_id(self):
        for order in self:
            template = self.sale_order_template_id

            if not order.note_header or order.note_header == "<p><br></p>":
                order.note_header = template.note_header

            if not order.note_footer or order.note_footer == "<p><br></p>":
                order.note_footer = template.note_footer
