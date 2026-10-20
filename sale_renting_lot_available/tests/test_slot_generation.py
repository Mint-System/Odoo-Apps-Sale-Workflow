# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo.fields import Command

from odoo.addons.sale.tests.common import SaleCommon


class TestStockRentalSlotGeneration(SaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.printer = cls.env["product.product"].create(
            {
                "name": "Test Printer",
                "type": "consu",
                "tracking": "serial",
                "rent_ok": True,
            }
        )
        cls.lots = cls.env["stock.lot"].create(
            [{"name": f"PRINTT{idx}", "product_id": cls.printer.id} for idx in range(1, 5)]
        )
        cls.order = (
            cls.env["sale.order"]
            .with_context(in_rental_app=True)
            .create(
                {
                    "partner_id": cls.partner.id,
                    "rental_start_date": datetime(2023, 1, 1, hour=9, minute=0),
                    "rental_return_date": datetime(2023, 1, 5, hour=18, minute=0),
                    "order_line": [
                        Command.create(
                            {
                                "product_id": cls.printer.id,
                                "product_uom_qty": 4,
                            }
                        )
                    ],
                }
            )
        )
        cls.line = cls.order.order_line[0]
        cls.line.is_rental = True
        cls.line.reserved_lot_ids = [(6, 0, cls.lots.ids)]
        cls.order.action_confirm()

    def test_generate_slots_for_partial_pickup(self):
        """A line with qty 4 and 3 lots picked up must get 4 slots."""
        self.line.write(
            {
                "qty_delivered": 3.0,
                "pickedup_lot_ids": [(6, 0, self.lots[:3].ids)],
            }
        )

        self.assertEqual(len(self.line.rental_slot_ids), 4)
        self.assertEqual(len(self.line.rental_slot_ids.filtered("lot_id")), 3)
        self.assertEqual(len(self.line.rental_slot_ids.filtered(lambda s: not s.lot_id)), 1)
        self.assertTrue(all(slot.lot_id in self.lots[:3] for slot in self.line.rental_slot_ids.filtered("lot_id")))

    def test_confirm_generates_slots_for_forced_rental_line(self):
        """Confirming must generate slots for lines whose is_rental was forced after creation."""
        so = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "rental_start_date": datetime(2023, 2, 1, hour=9, minute=0),
                "rental_return_date": datetime(2023, 2, 4, hour=18, minute=0),
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.printer.id,
                            "product_uom_qty": 2,
                        }
                    )
                ],
            }
        )
        line = so.order_line[0]
        # No rental app context: is_rental computes to False, so no slots yet
        self.assertFalse(line.is_rental)
        self.assertEqual(len(line.rental_slot_ids), 0)
        # Force is_rental after creation (demo/legacy path): still no slots
        line.is_rental = True
        self.assertEqual(len(line.rental_slot_ids), 0)
        # Confirmation must now generate the slots
        so.action_confirm()
        self.assertEqual(len(line.rental_slot_ids), 2)

    def test_slot_company_id(self):
        """Slots must be linked to the company of the sale order line."""
        self.line.write(
            {
                "qty_delivered": 3.0,
                "pickedup_lot_ids": [(6, 0, self.lots[:3].ids)],
            }
        )
        self.assertTrue(all(slot.company_id == self.line.company_id for slot in self.line.rental_slot_ids))

        # Placeholder slots created for lots get the lot (or fallback) company.
        placeholder = self.lots[0].rental_slot_ids.filtered("is_placeholder")[0]
        self.assertTrue(placeholder.company_id)
