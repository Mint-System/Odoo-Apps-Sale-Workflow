import datetime
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrderRecurrence(models.Model):
    _inherit = "sale.temporal.recurrence"

    period_discount_ids = fields.One2many(
        "sale.temporal.period_discount", "recurrence_id"
    )

    def get_period_discount(self, date=fields.Date.today()):
        return self.period_discount_ids.filtered(lambda p: date <= p.date)[:1]


class SaleOrderPeriodDiscount(models.Model):
    _name = "sale.temporal.period_discount"
    _desciption = "Period Discount"
    _order = "sequence"

    sequence = fields.Integer()
    name = fields.Char(compute="_compute_name")
    date = fields.Date(compute="_compute_date")
    recurrence_id = fields.Many2one("sale.temporal.recurrence", required=True)
    day = fields.Integer(default=1, required=True)
    month = fields.Selection(
        [
            ("1", "January"),
            ("2", "February"),
            ("3", "March"),
            ("4", "April"),
            ("5", "May"),
            ("6", "June"),
            ("7", "July"),
            ("8", "August"),
            ("9", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ],
        required=True,
        default=1,
    )
    discount = fields.Float(string="Discount (%)", digits="Discount", required=True)

    def _compute_date(self):
        for discount in self:
            discount.date = datetime.date(
                fields.Date.today().year, int(discount.month), discount.day
            )

    def _compute_name(self):
        for discount in self:
            discount.name = (
                str(fields.Date.today().year)
                + "-"
                + str(discount.month)
                + "-"
                + str(discount.day)
            )