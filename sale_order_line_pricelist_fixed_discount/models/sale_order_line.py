from odoo import fields, models, _, api
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.onchange('product_id', 'price_unit')
    def _onchange_price_rule(self):
        '''Filter and apply pricelist rule with fixed discount.'''

        # Read filter date from context
        date = self._context.get('date') or self.order_id.date_order or fields.Datetime.now() # or self.order_id.commitment_date

        # Filter rules from pricelist
        rule_ids = self.order_id.pricelist_id.item_ids.filtered(lambda r: 
            r.applied_on == '3_global' or 
            (r.applied_on == '0_product_variant' and r.product_id == self.product_id ) or 
            (r.applied_on == '1_product' and r.product_tmpl_id == self.product_template_id )
        ).sorted(lambda r: r.sequence)
        
        if rule_ids:
            
            # Get pricelist rule filtered by date                
            rule_ids_with_date = rule_ids.filtered(lambda l:
                (l.date_start and l.date_end and (l.date_start <= date <= l.date_end)) or
                (l.date_start and not l.date_end and l.date_start <= date) or
                (l.date_end and not l.date_start and date <= l.date_end)
            )
            # Get rules without date
            rule_ids_without_date = rule_ids.filtered(lambda l:
                (not l.date_start and not l.date_end)
            )

            # Select first rule with date and otherwise first rule without date
            rule_id = (rule_ids_with_date and rule_ids_with_date[0]) or (rule_ids_without_date and rule_ids_without_date[0])

            # _logger.warning([rule_id.name, rule_ids_with_date, rule_ids_without_date])

            # Apply fixed price discount
            if rule_id.price_discount != 0:
                # self.price_unit = rule_id.fixed_price
                self.discount = rule_id.price_discount
