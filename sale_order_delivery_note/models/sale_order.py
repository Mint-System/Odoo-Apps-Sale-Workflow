from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_note = fields.Text()

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for picking in self.picking_ids:
            picking.write({'delivery_note': self.delivery_note})
        return res

    @api.onchange('delivery_note')
    def _onchange_delivery_note(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([('id', 'in', rec.picking_ids.ids)])
            pickings.write({'delivery_note': rec.delivery_note})
