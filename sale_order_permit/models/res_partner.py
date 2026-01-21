import logging

from odoo import models
from odoo.http import request

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def _create_user_from_template(self, values):
        _logger.warning("### create user called")
        user = super()._create_user_from_template(values)
        _logger.warning(f"##user: {user}")

        pricelist_id = request.session.get('chosen_pricelist_id')
        _logger.warning(f"## pricelist: {pricelist_id}")
        if pricelist_id:
            user.partner_id.sudo().write({
                'property_product_pricelist': pricelist_id
            })
        request.session.pop('chosen_pricelist_id', None)

        return user