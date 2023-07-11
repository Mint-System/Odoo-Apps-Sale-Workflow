import logging
from odoo import fields, models, _, api
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.depends('partner_id')
    # def _compute_partner_invoice_id(self):
    #     res = super()._compute_partner_invoice_id()
    #     for order in self:
    #         if order.partner_id:
    #             partner_invoice_id = self.env['res.partner'].browse(order.partner_id.address_get(['invoice'])['invoice'])
    #             _logger.warning(partner_invoice_id)
    #             order.partner_invoice_id = partner_invoice_id.id if partner_invoice_id.street else False
    #     return res

    # @api.depends('partner_id')
    # def _compute_partner_shipping_id(self):
    #     res = super()._compute_partner_shipping_id()
    #     for order in self:
    #         if order.partner_id:
    #             partner_shipping_id = self.env['res.partner'].browse(order.partner_id.address_get(['delivery'])['delivery'])
    #             order.partner_shipping_id = partner_shipping_id.id if partner_shipping_id.street else False
    #     return res
