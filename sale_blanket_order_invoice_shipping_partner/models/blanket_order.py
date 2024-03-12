from odoo import fields, models, api


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    partner_invoice_id = fields.Many2one(
        "res.partner",
        string="Invoice Address",
        readonly=True,
        #required=True,
        states={"draft": [("readonly", False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    partner_shipping_id = fields.Many2one(
        "res.partner",
        string="Delivery Address",
        readonly=True,
        #required=True,
        states={"draft": [("readonly", False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Invoice address
        - Delivery address
        """
        super().onchange_partner_id()
        if not self.partner_id:
            self.partner_invoice_id = False
            self.partner_shipping_id = False
            return
        
        addr = self.partner_id.address_get(["delivery", "invoice"])
        values = {
            "partner_invoice_id": addr["invoice"],
            "partner_shipping_id": addr["delivery"],
        }
        self.update(values)
