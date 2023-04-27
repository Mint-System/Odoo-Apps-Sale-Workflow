from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id', 'date_order')
    def onchange_partner_id(self):        
        partner_id = self.partner_id.with_context(date=self.date_order)        
        values = {
            'pricelist_id': partner_id.property_product_pricelist and partner_id.property_product_pricelist.id or False,
        }       
        self.update(values)
        super().onchange_partner_id()