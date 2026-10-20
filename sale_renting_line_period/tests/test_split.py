# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

import odoo.exceptions
from odoo.fields import Command

from odoo.addons.sale.tests.common import SaleCommon


class TestRentalOrderLineWizard(SaleCommon):
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
                                "product_uom_qty": 3,
                            }
                        )
                    ],
                }
            )
        )
        cls.line = cls.order.order_line[0]
        cls.line.is_rental = True
        cls.line.reserved_lot_ids = [(6, 0, cls.lots[:3].ids)]
        cls.order.action_confirm()

    def _pickup(self):
        # Simulate the pickup wizard: mark 3 lots as picked up/delivered.
        self.line.write(
            {
                "qty_delivered": 3.0,
                "pickedup_lot_ids": [(6, 0, self.lots[:3].ids)],
            }
        )

    def test_split_line_per_qty(self):
        self._pickup()
        self.assertEqual(self.line.rental_status, "return")

        wizard = self.env["rental.order.line.wizard"].create(
            {
                "so_line_id": self.line.id,
                "product_uom_qty": self.line.product_uom_qty,
            }
        )
        new_lines = wizard.split()

        # Original line is kept plus one line for every additional unit.
        self.assertEqual(len(new_lines), 2)
        self.assertEqual(len(self.order.order_line), 3)
        self.assertTrue(all(line.product_uom_qty == 1 for line in self.order.order_line))
        self.assertTrue(all(line.id in new_lines.ids for line in new_lines))

        # Lots are distributed across the split lines, one lot per line.
        self.assertEqual(
            set(self.order.order_line.mapped("pickedup_lot_ids.id")),
            set(self.lots[:3].ids),
        )
        self.assertTrue(all(len(line.pickedup_lot_ids) == 1 for line in self.order.order_line))

        # Picked up lines must be in state 'return', not 'returned'.
        self.assertTrue(all(line.rental_status == "return" for line in self.order.order_line))

    def test_split_rejects_single_qty(self):
        self.line.product_uom_qty = 1.0
        wizard = self.env["rental.order.line.wizard"].create(
            {
                "so_line_id": self.line.id,
                "product_uom_qty": self.line.product_uom_qty,
            }
        )
        with self.assertRaises(odoo.exceptions.UserError):
            wizard.split()

    def test_split_rejects_returned_line(self):
        self._pickup()
        # Fully return the line.
        self.line.write(
            {
                "qty_returned": 3.0,
                "returned_lot_ids": [(6, 0, self.lots[:3].ids)],
            }
        )
        self.line.invalidate_recordset()
        self.assertEqual(self.line.rental_status, "returned")

        wizard = self.env["rental.order.line.wizard"].create(
            {
                "so_line_id": self.line.id,
                "product_uom_qty": self.line.product_uom_qty,
            }
        )
        with self.assertRaises(odoo.exceptions.UserError):
            wizard.split()
