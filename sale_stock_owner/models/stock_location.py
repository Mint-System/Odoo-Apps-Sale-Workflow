from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    clear_owner_id = fields.Boolean(default=False)
