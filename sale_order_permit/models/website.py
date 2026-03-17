import logging

from odoo import models
from odoo.http import request

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"


    def _get_current_pricelist(self):
        pricelist = super()._get_current_pricelist()

        if request.session.get("force_dummy_pricelist"):
            request.session.pop("force_dummy_pricelist", None)

            return request.env["product.pricelist"].search(
                [("sequence", "=", 0)], limit=1
            )

        return pricelist




