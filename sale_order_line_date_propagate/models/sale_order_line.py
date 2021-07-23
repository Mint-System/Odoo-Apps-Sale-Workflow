import logging

from odoo import models, fields
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, values):
        _logger.info(values)
        if values.get('commitment_date'):
             self.move_ids.date = fields.Datetime.to_datetime(values.get('commitment_date')) - relativedelta(days=self.company_id.security_lead)
        return super(SaleOrderLine, self).write(values)
