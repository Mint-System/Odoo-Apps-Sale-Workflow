from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    clear_owner = fields.Boolean(default=False)
