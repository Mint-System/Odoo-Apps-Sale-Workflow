# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockLotRental(models.Model):
    _name = "stock.lot.rental"
    _description = "Stock Lot Rental"

    name = fields.Char(compute="_compute_name", store=True, readonly=True)
    active = fields.Boolean(default=True)

    # Stock link

    lot_id = fields.Many2one("stock.lot")
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

    # Sale link

    so_line_id = fields.Many2one("sale.order.line", string="Sale Order Line")
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

    @api.depends("sale_order_id.name", "product_id.name", "lot_id.name", "start_date", "return_date")
    def _compute_name(self):
        for record in self:
            order_name = record.sale_order_id.name or ""
            product_name = record.product_id.name or ""
            lot_name = record.lot_id.name or ""
            start = fields.Date.to_string(record.start_date.date()) if record.start_date else ""
            end = fields.Date.to_string(record.return_date.date()) if record.return_date else ""
            record.name = f"{order_name} - {product_name} - {lot_name}: {start} - {end}"
