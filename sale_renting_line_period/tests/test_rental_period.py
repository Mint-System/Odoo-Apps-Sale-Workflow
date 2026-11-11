# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo.fields import Command

from odoo.addons.sale.tests.common import SaleCommon


class TestRentalPeriod(SaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.printer = cls.env["product.product"].create(
            {
                "name": "Period Printer",
                "type": "consu",
                "tracking": "serial",
                "rent_ok": True,
            }
        )
        cls.lots = cls.env["stock.lot"].create(
            [{"name": f"PERIOD{idx}", "product_id": cls.printer.id} for idx in range(1, 3)]
        )
        cls.order = (
            cls.env["sale.order"]
            .with_context(in_rental_app=True)
            .create(
                {
                    "partner_id": cls.partner.id,
                    "rental_start_date": datetime(2026, 12, 1, hour=9),
                    "rental_return_date": datetime(2026, 12, 5, hour=18),
                    "order_line": [
                        Command.create(
                            {
                                "product_id": cls.printer.id,
                                "product_uom_qty": 2,
                            }
                        )
                    ],
                }
            )
        )
        cls.line = cls.order.order_line[0]
        cls.line.is_rental = True
        cls.line.reserved_lot_ids = [Command.set(cls.lots.ids)]
        cls.order.action_confirm()

    def test_return_date_is_end_of_day(self):
        """The line return date must be the last second of the return day."""
        self.assertEqual(self.line.rental_return_date, datetime(2026, 12, 5, hour=23, minute=59, second=59))

    def test_return_date_is_end_of_day_in_user_timezone(self):
        """The end of day is calculated in the user timezone, not in UTC."""
        # 2026-12-05 18:00 UTC is 2026-12-05 19:00 in Europe/Berlin
        line = self.line.with_context(tz="Europe/Berlin")
        self.assertEqual(
            line._get_rental_return_date(datetime(2026, 12, 5, hour=18)), datetime(2026, 12, 5, 22, 59, 59)
        )
        # 2026-12-05 23:30 UTC is already 2026-12-06 in Europe/Berlin
        self.assertEqual(
            line._get_rental_return_date(datetime(2026, 12, 5, hour=23, minute=30)), datetime(2026, 12, 6, 22, 59, 59)
        )

    def test_return_date_follows_order(self):
        """Extending the order period must update the line return date."""
        self.order.write({"rental_return_date": datetime(2026, 12, 9, hour=10)})
        self.line.invalidate_recordset()
        self.assertEqual(self.line.rental_return_date, datetime(2026, 12, 9, hour=23, minute=59, second=59))

    def test_returned_line_keeps_return_date(self):
        """A returned line must keep its own return date."""
        self.line.write(
            {
                "qty_delivered": 2.0,
                "pickedup_lot_ids": [Command.set(self.lots.ids)],
            }
        )
        self.line.write({"rental_return_date": datetime(2026, 12, 4, hour=12)})
        self.line.write(
            {
                "qty_returned": 2.0,
                "returned_lot_ids": [Command.set(self.lots.ids)],
            }
        )
        self.line.invalidate_recordset()
        self.assertEqual(self.line.rental_status, "returned")

        self.order.write({"rental_return_date": datetime(2026, 12, 20, hour=10)})
        self.line.invalidate_recordset()
        self.assertEqual(self.line.rental_return_date, datetime(2026, 12, 4, hour=12))
