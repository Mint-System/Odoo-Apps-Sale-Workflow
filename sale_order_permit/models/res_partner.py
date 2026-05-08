import logging

from odoo import fields, models
from odoo.http import request

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def _create_user_from_template(self, values):
        user = super()._create_user_from_template(values)

        pricelist_id = request.session.get("chosen_pricelist_id")
        if pricelist_id:
            user.partner_id.sudo().write({"property_product_pricelist": pricelist_id})
        request.session.pop("chosen_pricelist_id", None)

        return user


class ResPartner(models.Model):
    _inherit = "res.partner"

    permit_number = fields.Char(
        readonly=True,
        copy=False,
        index=True,
    )

    _sql_constraints = [
        (
            "permit_number_unique",
            "unique(permit_number)",
            "Permit number must be unique.",
        )
    ]
