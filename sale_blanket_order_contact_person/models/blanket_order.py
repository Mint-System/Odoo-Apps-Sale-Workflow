from odoo import api, fields, models


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    partner_contact_id = fields.Many2one(
        "res.partner", string="Contact Person", states={"draft": [("readonly", False)]}
    )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        res = super().onchange_partner_id()
        addr = self.partner_id.address_get(["sale"])
        values = {
            "partner_contact_id": addr["sale"],
        }
        self.update(values)
        return res
