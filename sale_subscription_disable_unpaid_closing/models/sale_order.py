# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _skip_unpaid_close(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'sale_subscription_disable_unpaid_closing.skip_unpaid_subscription_close', 'True'
        ) == 'True'

    def _skip_expired_close(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'sale_subscription_disable_unpaid_closing.skip_expired_subscription_close', 'True'
        ) == 'True'


    def _handle_unpaid_subscriptions(self):
        if self._skip_unpaid_close():
            return {}
        return super()._handle_unpaid_subscriptions()

    def _get_expired_subscriptions(self):
        if self._skip_expired_close():
            return []
        expired_result = super()._get_expired_subscriptions()
        if self._skip_unpaid_close():
            unpaid_ids = {r['so_id'] for r in self._get_unpaid_subscriptions()}
            expired_result = [r for r in expired_result if r['so_id'] not in unpaid_ids]
        return expired_result
