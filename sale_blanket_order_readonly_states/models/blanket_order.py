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

    partner_id = fields.Many2one(states=READONLY_STATES)
    pricelist_id = fields.Many2one(states=READONLY_STATES)
    analytic_account_id = fields.Many2one(states=READONLY_STATES)
    payment_term_id = fields.Many2one(states=READONLY_STATES)
    validity_date = fields.Date(states=READONLY_STATES)
    client_order_ref = fields.Char(states=READONLY_STATES)
    note = fields.Text(states=READONLY_STATES)
    user_id = fields.Many2one(states=READONLY_STATES)
    team_id = fields.Many2one(states=READONLY_STATES)
    company_id = fields.Many2one(states=READONLY_STATES)
