from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # @api.model
    # def create(self, vals):
    #     """Calculate commitment date from expected date."""
    #     res = super(SaleOrderLine, self).create(vals)
    #     _logger.warning(['CREATE ORDER LINE'])
    #     for line in res:
    #         _logger.warning(['SET COMMITMENT DATE', line._expected_date()])
    #         line.write({"commitment_date": line._expected_date()})
    #     return res

    @api.onchange('customer_lead', 'product_id')
    def _onchange_customer_lead_set_commitment_date(self):
        # _logger.warning(['SET COMMITMENT DATE', self._expected_date()])
        if self.product_id:
            self.write({"commitment_date": self._expected_date()})

    # @api.onchange('product_id')
    # def _onchange_product_id_set_customer_lead(self):
    #     _logger.warning(['TRIGGER CUSTOMER LEAD'])
    #     self._onchange_customer_lead_set_commitment_date()
        # if self.customer_lead == 0.0 and self.product_id:
        #     self.write({"commitment_date": self._expected_date()})

    # def write(self, vals):
    #     for line in self:
    #         _logger.warning(['SET COMMITMENT DATE', line._expected_date()])
    #         vals.update({"commitment_date": line._expected_date()})
    #     return super(SaleOrderLine, self).write(vals)


# class SaleOrder(models.Model):
#     _inherit = "sale.order"

#     @api.depends('order_line.customer_lead', 'date_order', 'order_line.state')
#     def _compute_expected_date(self):
#         super()._compute_expected_date()
#         for order in self:
#             if not order.commitment_date:
#                 order.commitment_date = order.expected_date

#     def copy(self, default=None):
#         res = super().copy(default=default)
#         res._compute_expected_date()
#         return res