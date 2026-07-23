# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockRentalSlot(models.Model):
    _name = "stock.rental.slot"
    _description = "Stock Rental Slot"

    name = fields.Char(compute="_compute_name", store=True, readonly=True)
    active = fields.Boolean(default=True)

    # Stock link

    product_id = fields.Many2one(
        "product.product",
        compute="_compute_product_id",
        store=True,
        readonly=True,
    )
    categ_id = fields.Many2one(
        "product.category",
        related="product_id.categ_id",
        store=True,
        readonly=True,
    )
    lot_id = fields.Many2one("stock.lot", readonly=True)

    # Sale link

    so_line_id = fields.Many2one("sale.order.line", string="Sale Order Line", readonly=True)
    rental_color = fields.Integer(related="so_line_id.rental_color")
    order_partner_id = fields.Many2one(
        related="so_line_id.order_partner_id",
        string="Customer",
        store=True,
        readonly=True,
    )
    rental_status = fields.Selection(
        related="so_line_id.rental_status",
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
        compute="_compute_dates",
        inverse="_inverse_dates",
        store=True,
    )
    return_date = fields.Datetime(
        compute="_compute_dates",
        inverse="_inverse_dates",
        store=True,
    )
    duration_days = fields.Integer(
        related="so_line_id.duration_days",
    )

    @api.depends("lot_id", "so_line_id")
    def _compute_product_id(self):
        for record in self:
            if record.so_line_id:
                record.product_id = record.so_line_id.product_id
            elif record.lot_id:
                record.product_id = record.lot_id.product_id
            else:
                record.product_id = False

    @api.depends("so_line_id", "so_line_id.rental_start_date", "so_line_id.rental_return_date")
    def _compute_dates(self):
        now = fields.Datetime.now()
        for record in self:
            record.start_date = record.so_line_id.rental_start_date or now
            record.return_date = record.so_line_id.rental_return_date or now

    def _inverse_dates(self):
        for record in self:
            if record.so_line_id:
                record.so_line_id.rental_start_date = record.start_date
                record.so_line_id.rental_return_date = record.return_date

    @api.depends(
        "sale_order_id.name",
        "order_partner_id.name",
        "product_id.name",
        "lot_id.name",
        "start_date",
        "return_date",
    )
    def _compute_name(self):
        for record in self:
            if record.sale_order_id:
                record.name = f"{record.sale_order_id.display_name} - {record.order_partner_id.name}"
            elif record.lot_id:
                record.name = f"{record.product_id.name} - {record.lot_id.name}"

    def action_show_stock_rental_slot_period(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Filter Period",
            "res_model": "stock.rental.slot.period",
            "view_mode": "form",
            "target": "new",
            "view_id": self.env.ref("sale_renting_lot_available.stock_rental_slot_period_form_view").id,
        }

    def action_create_order(self):
        """Open a blank sale order form pre-filled with the selected slots' products."""
        products = self.mapped("product_id")
        if not products:
            raise UserError(_("Selected slots have no product."))

        order_lines = []
        for product in products:
            order_lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": product.id,
                        "product_uom_qty": 1,
                    },
                )
            )

        return {
            "type": "ir.actions.act_window",
            "name": _("Sale Order"),
            "res_model": "sale.order",
            "view_mode": "form",
            "context": {
                "default_order_line": order_lines,
                "in_rental_app": 1,
            },
        }

    def action_view_order(self):
        self.ensure_one()
        if not self.sale_order_id:
            return {}
        return {
            "type": "ir.actions.act_window",
            "name": _("Sale Order"),
            "res_model": "sale.order",
            "view_mode": "form",
            "res_id": self.sale_order_id.id,
        }

    def action_split_order_line(self):
        raise UserError(_("This action is not yet available."))
