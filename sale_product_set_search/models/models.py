import logging

from odoo import api, models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class ProductSet(models.Model):
    _inherit = "product.set"

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, order=None, name_get_uid=None):
    # def _name_search(
    #     self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    # ):
        args = args or []
        if operator == "ilike" and not (name or "").strip():
            domain = []
        else:
            domain = ["|", ("name", "ilike", name), ("ref", "ilike", name)]
        return self._search(
            expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
        )
