from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta, datetime

class SaleOrder(models.Model):
    _inherit = "sale.order"

    commitment_date = fields.Datetime('Delivery Date', copy=False,
        default=lambda self: self._get_default_commitment_date(),
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="This is the delivery date promised to the customer. "
            "If set, the delivery order will be scheduled based on "
            "this date rather than product lead times.")

    def _get_default_commitment_date(self):
        _logger.info(f"Current time is: {datetime.now()}")
        # Add 1 day before noon and 2 days after
        if datetime.now().hour < 12:
            commitment_date = datetime.now() + timedelta(days=1)
        else:
            commitment_date = datetime.now() + timedelta(days=2)
        # Set time and return
        return commitment_date.replace(hour=9, minute=57)