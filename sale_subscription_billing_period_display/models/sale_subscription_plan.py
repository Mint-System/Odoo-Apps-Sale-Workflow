import logging
from odoo import api, fields, models, _
from odoo import http

_logger = logging.getLogger(__name__)


class SaleSubscriptionPlan(models.Model):
    _inherit = 'sale.subscription.plan'


    @api.depends('billing_period_value', 'billing_period_unit')
    def _compute_billing_period_display(self):
        for plan in self:
            unit = plan.billing_period_unit
            value = plan.billing_period_value

            if value == 1:
                plan.billing_period_display = _("1 %s") % unit
            else:
                plan.billing_period_display = _("%(value)s %(unit)s") % {
                    'value': value,
                    'unit': unit + 's'
                }