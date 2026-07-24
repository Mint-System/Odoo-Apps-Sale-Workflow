# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = "stock.lot"

    rental_slot_ids = fields.One2many("stock.rental.slot", "lot_id", string="Rental Slots")
    start_slot_id = fields.Many2one("stock.rental.slot")
    # end_slot_id = fields.Many2one("stock.rental.slot")

    rental_slot_count = fields.Integer(
        compute="_compute_rental_slot_count",
        string="Rental Slots",
    )

    @api.depends("rental_slot_ids")
    def _compute_rental_slot_count(self):
        for lot in self:
            lot.rental_slot_count = len(lot.rental_slot_ids)

    def action_view_rental_slots(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Rental Slots"),
            "res_model": "stock.rental.slot",
            "view_mode": "gantt,list,form",
            "context": {
                "search_default_lot_id": self.id,
                "search_default_groupby_product": 1,
                "search_default_groupby_lot": 1,
            },
        }

    def _create_stock_rental_lot(self):
        """
        Create a placeholder stock.rental.slot entry for gantt range.
        """
        for lot in self:
            if lot.product_id.rent_ok:
                lot.start_slot_id = lot.env["stock.rental.slot"].create({"lot_id": lot.id})
                # lot.end_slot_id = lot.env["stock.rental.slot"].create({"lot_id": lot.id})

    @api.model_create_multi
    def create(self, vals_list):
        lots = super().create(vals_list)
        lots._create_stock_rental_lot()
        return lots

    def unlink(self):
        self.rental_slot_ids.sudo().unlink()
        return super().unlink()

    def toggle_active(self):
        super().toggle_active()
        self.rental_slot_ids.active = self.active
