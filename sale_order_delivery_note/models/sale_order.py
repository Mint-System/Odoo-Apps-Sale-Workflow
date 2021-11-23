from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_note = fields.Text()

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrder, self)._prepare_procurement_values(group_id)
        res.update({'delivery_note': self.delivery_note})
        return res
