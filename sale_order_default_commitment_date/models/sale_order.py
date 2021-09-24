from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta, datetime
from pytz import timezone, UTC

class SaleOrder(models.Model):
    _inherit = "sale.order"

    commitment_date = fields.Datetime('Delivery Date', copy=False,
        default=lambda self: self._get_default_commitment_date(),
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="This is the delivery date promised to the customer. "
            "If set, the delivery order will be scheduled based on "
            "this date rather than product lead times.")

    def _get_default_commitment_date(self):
        
        # Get now with timezone
        now = datetime.now().replace(tzinfo=UTC).astimezone(timezone(self.env.user.tz or 'UTC')).replace(tzinfo=None)

        # Add 1 day before noon and 2 days after
        if now.hour < 12:
            commitment_date = now + timedelta(days=1)
        else:
            commitment_date = now + timedelta(days=2)

        # Set default time
        commitment_date = commitment_date.replace(hour=7, minute=57)

        # _logger.info(f'{commitment_date}')

        return commitment_date