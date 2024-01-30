import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_ref = fields.Char(related="partner_id.ref", string="Customer No.")
