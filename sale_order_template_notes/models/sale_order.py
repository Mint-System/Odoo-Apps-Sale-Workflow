import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("sale_order_template_id")
    def _onchange_sale_order_template_id(self):
        res = super(SaleOrder, self)._onchange_sale_order_template_id()
        # if notes are set in template overwrite the order notes
        if self.sale_order_template_id.note_header:
            self.note_header = self.sale_order_template_id.note_header
        if self.sale_order_template_id.note_footer:
            self.note_footer = self.sale_order_template_id.note_footer
        return res
