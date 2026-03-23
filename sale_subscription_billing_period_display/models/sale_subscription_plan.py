import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class SaleSubscriptionPlan(models.Model):
    _inherit = "sale.subscription.plan"

    # @api.depends('billing_period_value', 'billing_period_unit')
    # def _compute_billing_period_display(self):
    #     for plan in self:
    #         unit = plan.billing_period_unit
    #         value = plan.billing_period_value

    #         if value == 1:
    #             plan.billing_period_display = _("1 %s") % unit
    #         else:
    #             plan.billing_period_display = _("%(value)s %(unit)s") % {
    #                 'value': value,
    #                 'unit': unit + 's'
    #             }

    @api.depends("billing_period_value", "billing_period_unit")
    def _compute_billing_period_display(self):
        for plan in self:
            unit = plan.billing_period_unit
            value = plan.billing_period_value

            # translations and plural forms
            unit_translations = {
                "day": {
                    "singular": _("day"),
                    "plural": _("days"),
                },
                "week": {
                    "singular": _("week"),
                    "plural": _("weeks"),
                },
                "month": {
                    "singular": _("month"),
                    "plural": _("months"),
                },
                "year": {
                    "singular": _("year"),
                    "plural": _("years"),
                },
            }

            # Get translated unit
            unit_info = unit_translations.get(
                unit,
                {
                    "singular": unit,
                    "plural": unit + "s",
                },
            )

            if value == 1:
                plan.billing_period_display = _("1 %s") % unit_info["singular"]
            else:
                plan.billing_period_display = _("%s %s") % (value, unit_info["plural"])
