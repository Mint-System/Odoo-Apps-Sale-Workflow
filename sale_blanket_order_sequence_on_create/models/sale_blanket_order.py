# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class BlanketOrder(models.Model):
    _inherit = "sale.blanket.order"


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Draft") == "Draft":
                sequence_obj = self.env["ir.sequence"]
                company_id = vals.get("company_id")
                if company_id:
                    sequence_obj = sequence_obj.with_company(company_id)
                vals["name"] = sequence_obj.next_by_code("sale.blanket.order") or "Draft"
        return super().create(vals_list)


    def action_confirm(self):
        self._validate()
        for order in self:
            order.write({"confirmed": True})
        return True


