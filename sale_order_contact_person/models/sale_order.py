import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_contact_id = fields.Many2one("res.partner", string="Sale Contact Address")

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        res = super().onchange_partner_id()
        addr = self.partner_id.address_get(["sale"])
        values = {
            "partner_contact_id": addr["sale"],
        }
        self.update(values)
        return res

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        if "partner_sale_id" in self.env["account.move"]._fields:
            moves.write({"partner_sale_id": self.partner_contact_id.id})
        return moves
