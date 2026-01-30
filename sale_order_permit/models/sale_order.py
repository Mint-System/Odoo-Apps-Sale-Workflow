import logging
from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        # no sale order if date is after March 31
        today = date.today()
        limit_date = date(today.year, 3, 31)

        for order in self:
            product = order.order_line[0].product_id
            for line in order.order_line:
                if (
                    product.duration == "year"
                    and line.date_from
                    and line.date_from > limit_date
                ):
                    raise ValidationError(
                        _("Sie können kein Jahrespatent mehr nach dem (%s) kaufen.")
                        % limit_date
                    )

        res = super().action_confirm()

        seq = self.env.ref("sale_order_permit.seq_permit_number")
        for order in self:
            product = order.order_line[0].product_id
            if not order.partner_id.permit_number and product.duration == "year":
                order.partner_id.permit_number = seq.next_by_id()

        return res
