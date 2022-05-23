from odoo import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)

class BlanketOrder(models.Model):
    _inherit = ['sale.blanket.order']

    sale_order_template_id = fields.Many2one(
        'sale.order.template', 'Blanket Order Template Reference',
        ondelete='cascade', index=True)

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):

        template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)

        if not self.note_header or self.note_header == '<p><br></p>':
            self.note_header = template.note_header

        if not self.note_footer or self.note_footer == '<p><br></p>':
            self.note_footer = template.note_footer