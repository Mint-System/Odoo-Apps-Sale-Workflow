from odoo import api, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    @api.model
    def _is_tokenization_required(self, sale_order_id=None, **kwargs):
        """Do not force payment tokenization for order with subscriptions."""

        if sale_order_id:
            sale_order = self.env["sale.order"].browse(sale_order_id).exists()
            if sale_order.is_subscription or sale_order.subscription_id.is_subscription:
                return False
        return super()._is_tokenization_required(sale_order_id=sale_order_id, **kwargs)
