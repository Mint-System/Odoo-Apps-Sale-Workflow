import logging
from odoo import models, fields
from dateutil.relativedelta import relativedelta
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, values):
        """Update commitment and deadline date on moves"""
        commitment_date = values.get('commitment_date')
        if commitment_date:
             self.move_ids.date = fields.Datetime.to_datetime(commitment_date) - relativedelta(days=self.company_id.security_lead)
             self.move_ids.date_deadline = commitment_date
        return super(SaleOrderLine, self).write(values)
