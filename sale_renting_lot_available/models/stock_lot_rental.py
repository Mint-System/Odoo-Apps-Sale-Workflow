# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class StockLotRental(models.Model):
    _name = "stock.lot.rental"
    _description = "Stock Lot Rental"
    _rec_name = "lot_id"

    lot_id = fields.Many2one("stock.lot", required=True)
    product_id = fields.Many2one(
        "product.product",
        related="lot_id.product_id",
        store=True,
        readonly=True,
    )
    categ_id = fields.Many2one(
        "product.category",
        related="product_id.categ_id",
        store=True,
        readonly=True,
    )
    so_line_id = fields.Many2one("sale.order.line", required=True, string="Sale Order Line")
    rental_status = fields.Selection(
        related="so_line_id.rental_status",
        store=True,
        readonly=True,
    )
    is_late = fields.Boolean(
        related="so_line_id.is_late",
        store=True,
        readonly=True,
    )
    sale_order_id = fields.Many2one(
        "sale.order",
        related="so_line_id.order_id",
        store=True,
        readonly=True,
    )
    start_date = fields.Datetime(
        related="so_line_id.rental_start_date",
        store=True,
        readonly=True,
    )
    return_date = fields.Datetime(
        related="so_line_id.rental_return_date",
        store=True,
        readonly=True,
    )
