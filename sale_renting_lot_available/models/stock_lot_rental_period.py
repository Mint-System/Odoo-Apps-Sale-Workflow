# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class StockLotRentalPeriod(models.Model):
    _name = "stock.lot.rental.period"
    _description = "Stock Lot Rental Period"

    start_date = fields.Datetime(required=True)
    return_date = fields.Datetime(required=True)
