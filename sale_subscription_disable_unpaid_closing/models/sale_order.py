# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _handle_unpaid_subscriptions(self):
        return {}


    def _get_expired_subscriptions(self):
        expired_result = super()._get_expired_subscriptions()
        unpaid_ids = {r['so_id'] for r in self._get_unpaid_subscriptions()}
        return [r for r in expired_result if r['so_id'] not in unpaid_ids]
