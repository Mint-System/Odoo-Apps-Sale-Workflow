import logging
from datetime import datetime, date, timedelta

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

from .config import DURATION_SELECTION


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_from = fields.Date(
        string='Start Date', required=True,
        help='Start Date of Patent',
        default=fields.Date.today()
        )

    date_to = fields.Date(
        compute="_compute_date_to")



    @api.onchange('product_id')
    def _onchange_product_id_date_from(self):
        for line in self:
            if not line.product_id:
                continue

            if line.product_id.duration == 'year':
                today = fields.Date.context_today(line)
                october_1 = date(today.year, 10, 1)

                year = today.year + 1 if today > october_1 else today.year
                line.date_from = datetime(year, 1, 1)
            else:
                line.date_from = fields.Datetime.now()



    @api.depends("date_from")
    def _compute_date_to(self):
        duration_map = {
            "year": {"days": 365},
            "day": {"days": 1},
            "week": {"weeks": 1},
        }
        for line in self:
            duration = line.product_id.duration
            _logger.warning(f"duration: {duration}")
            if line.date_from and line.product_id.duration in duration_map.keys():
               line.date_to = line.date_from + timedelta(**duration_map[duration])
            else:
                line.date_to = line.date_from




