import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _get_fixed_discount(self, product_id, product_uom_qty, date=None):
        """This method returns the fixed discount value."""

        # Filter rules from pricelist
        rule_ids = self.item_ids.filtered(
            lambda r: r.applied_on == "3_global"
            or (r.applied_on == "0_product_variant" and r.product_id == product_id)
            or (
                r.applied_on == "1_product"
                and r.product_tmpl_id == product_id.product_tmpl_id
            )
        ).sorted(lambda r: r.sequence)

        if rule_ids:

            # Get pricelist rule filtered by date
            rule_ids_with_date = rule_ids.filtered(
                lambda l: (
                    l.date_start and l.date_end and (l.date_start <= date <= l.date_end)
                )
                or (l.date_start and not l.date_end and l.date_start <= date)
                or (l.date_end and not l.date_start and date <= l.date_end)
            )

            # Get rules without date
            rule_ids_without_date = rule_ids.filtered(
                lambda l: (not l.date_start and not l.date_end)
            )

            # Select first rule with date, otherwise first rule without date
            rule_ids = rule_ids_with_date or rule_ids_without_date

            # Get pricelist rule filtered by minimum quantity
            rule_ids_with_min_qty = rule_ids.filtered(
                lambda l: l.min_quantity and (l.min_quantity <= product_uom_qty)
            ).sorted(lambda r: r.min_quantity)

            # Get rules without minimum quantity
            rule_ids_without_min_qty = rule_ids.filtered(lambda l: not l.min_quantity)

            # Select first rule with minimum quantity, otherwise first rule without minimum quantity
            rule_id = (rule_ids_with_min_qty and rule_ids_with_min_qty[-1][0]) or (
                rule_ids_without_min_qty and rule_ids_without_min_qty[0]
            )

            return rule_id.price_discount or 0.0

        else:

            return 0.0
