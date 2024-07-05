from odoo import api, fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    partner_invoice_id = fields.Many2one(
        "res.partner",
        string="Invoice Address",
        readonly=True,
        states={"draft": [("readonly", False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        compute="_compute_partner_invoice_id",
        store=True,
    )
    partner_shipping_id = fields.Many2one(
        "res.partner",
        string="Delivery Address",
        readonly=True,
        states={"draft": [("readonly", False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        compute="_compute_partner_shipping_id",
        store=True,
    )

    @api.depends("partner_id")
    def _compute_partner_invoice_id(self):
        for order in self:
            if order.partner_id:
                addr = order.partner_id.address_get(["invoice"])
                order.partner_invoice_id = addr.get("invoice", False)
            else:
                order.partner_invoice_id = False

    @api.depends("partner_id")
    def _compute_partner_shipping_id(self):
        for order in self:
            if order.partner_id:
                addr = order.partner_id.address_get(["delivery"])
                order.partner_shipping_id = addr.get("delivery", False)
            else:
                order.partner_shipping_id = False
