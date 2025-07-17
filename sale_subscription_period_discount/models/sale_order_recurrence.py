import datetime
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderRecurrence(models.Model):
    _inherit = "sale.temporal.recurrence"

    period_discount_ids = fields.One2many("sale.temporal.period_discount", "recurrence_id")

    def get_period_discount(self, date=fields.Date.today()):
        """
        Return first matching discount starting from date until end of year.
        """
        return self.period_discount_ids.filtered(lambda p: p.from_date <= date and p.from_date.year == date.year)[:1]


class SaleOrderPeriodDiscount(models.Model):
    _name = "sale.temporal.period_discount"
    _description = "Period Discount"
    _order = "month desc, day desc"

    name = fields.Char(compute="_compute_name")
    from_date = fields.Date(compute="_compute_from_date")
    recurrence_id = fields.Many2one("sale.temporal.recurrence", required=True)
    day = fields.Integer(default=1, required=True)
    month = fields.Selection(
        [
            ("01", "January"),
            ("02", "February"),
            ("03", "March"),
            ("04", "April"),
            ("05", "May"),
            ("06", "June"),
            ("07", "July"),
            ("08", "August"),
            ("09", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ],
        required=True,
        default=1,
    )
    year = fields.Integer(default=0, required=True, help="This number will be added to the current year.")
    discount = fields.Float(string="Discount (%)", digits="Discount", required=True)

    @api.depends("day", "month")
    def _compute_from_date(self):
        for discount in self:
            discount.from_date = datetime.date(
                fields.Date.today().year + discount.year, int(discount.month), discount.day
            )

    def _compute_name(self):
        for discount in self:
            discount.name = (
                str(fields.Date.today().year + discount.year) + "-" + str(discount.month) + "-" + str(discount.day)
            )
