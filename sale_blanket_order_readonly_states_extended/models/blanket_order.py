import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class BlanketOrder(models.Model):
    _inherit = ["sale.blanket.order"]

    READONLY_STATES = {
        "draft": [("readonly", False)],
        "sent": [("readonly", False)],
        "open": [("readonly", False)],
        "done": [("readonly", True)],
        "expired": [("readonly", True)],
        "cancel": [("readonly", True)],
    }

    partner_invoice_id = fields.Many2one(states=READONLY_STATES)
    partner_shipping_id = fields.Many2one(states=READONLY_STATES)
    partner_contact_id = fields.Many2one(states=READONLY_STATES)
    picking_policy = fields.Selection(states=READONLY_STATES)
