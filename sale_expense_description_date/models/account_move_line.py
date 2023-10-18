import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _sale_prepare_sale_line_values(self, order, price):
        res = super()._sale_prepare_sale_line_values(order, price)
        if self.expense_id:
            lang = self.env["res.lang"].search(
                [("code", "=", self.env.user.lang or "en_US")]
            )
            date_format = lang and lang.date_format or "%m/%d/%Y"
            res.update(
                {
                    "name": self.name
                    + " (%s)" % self.expense_id.date.strftime(date_format)
                }
            )
        return res
