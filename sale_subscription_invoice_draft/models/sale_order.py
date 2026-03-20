import logging
from odoo import models

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _should_post_invoice(self):
    	return False