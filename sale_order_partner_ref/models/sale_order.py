# import logging

# from odoo import _, api, fields, models

# _logger = logging.getLogger(__name__)

# class SaleOrder(models.Model):
#     #_name = 'sale_order_partner_ref'
#     # _description = 'Sale Order Partner Ref'
#     _inherits = "sale.order"

#     # name = fields.Char()
#     # values = fields.Integer()
#     # ref = fields.Char(string='Reference', index=True)
#     partner_ref = fields.Char(related="partner_id.ref")

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_ref = fields.Char(related="partner_id.ref")
