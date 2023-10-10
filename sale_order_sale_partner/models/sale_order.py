import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_sale_id = fields.Many2one(
        "res.partner",
        string="Sale Contact Address",
        compute="_compute_partner_sale_id",
        store=True,
        readonly=False,
        precompute=True,
    )

    @api.depends("partner_id")
    def _compute_partner_sale_id(self):
        for order in self:
            order.partner_sale_id = (
                self.partner_id.address_get(["sale"])["sale"]
                if order.partner_id
                else False
            )

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        if "partner_sale_id" in self.env["account.move"]._fields:
            moves.write({"partner_sale_id": self.partner_sale_id.id})
        return moves
