# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo.fields import Command

from odoo.addons.sale.tests.common import SaleCommon


class TestStockRentalSlotAvailability(SaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.printer = cls.env["product.product"].create(
            {
                "name": "Availability Printer",
                "type": "consu",
                "is_storable": True,
                "tracking": "serial",
                "rent_ok": True,
            }
        )
        cls.lots = cls.env["stock.lot"].create(
            [{"name": f"AVAIL{idx}", "product_id": cls.printer.id} for idx in range(1, 6)]
        )
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        for lot in cls.lots:
            cls.env["stock.quant"].create(
                {
                    "product_id": cls.printer.id,
                    "lot_id": lot.id,
                    "location_id": cls.stock_location.id,
                    "quantity": 1.0,
                }
            )

    def _create_order(self, start_date, end_date, qty=1):
        order = (
            self.env["sale.order"]
            .with_context(in_rental_app=True)
            .create(
                {
                    "partner_id": self.partner.id,
                    "rental_start_date": start_date,
                    "rental_return_date": end_date,
                    "order_line": [Command.create({"product_id": self.printer.id, "product_uom_qty": qty})],
                }
            )
        )
        order.order_line.is_rental = True
        order.action_confirm()
        return order

    def _get_available_count(self, start_date, end_date):
        period = self.env["stock.rental.slot.period"].create({"start_date": start_date, "end_date": end_date})
        return len(period.get_available_slot_ids())

    def test_max_overlap_of_non_overlapping_slots(self):
        """Slots that only touch the boundaries do not overlap."""
        slots = self.env["stock.rental.slot"]
        for start_date, end_date in [
            (datetime(2026, 12, 1), datetime(2027, 2, 1)),
            (datetime(2026, 12, 1), datetime(2027, 8, 31)),
            (datetime(2027, 7, 1), datetime(2027, 8, 31)),
        ]:
            slots |= self.env["stock.rental.slot"].create(
                {"product_id": self.printer.id, "start_date": start_date, "return_date": end_date}
            )
        self.assertEqual(self.env["stock.rental.slot"]._get_max_overlap(slots), 2)

    def test_available_slots_with_non_overlapping_bookings(self):
        """Only two of three bookings overlap, so three of five slots stay available."""
        self._create_order(datetime(2026, 12, 1), datetime(2027, 2, 1))
        self._create_order(datetime(2026, 12, 1), datetime(2027, 8, 31))
        self._create_order(datetime(2027, 7, 1), datetime(2027, 8, 31))

        self.assertEqual(self._get_available_count(datetime(2027, 1, 1), datetime(2027, 7, 31)), 3)

    def test_available_slots_with_overlapping_bookings(self):
        """All bookings overlap, so the available count is reduced by all of them."""
        self._create_order(datetime(2026, 12, 1), datetime(2027, 8, 31))
        self._create_order(datetime(2026, 12, 1), datetime(2027, 8, 31))
        self._create_order(datetime(2027, 1, 1), datetime(2027, 7, 31))

        self.assertEqual(self._get_available_count(datetime(2027, 1, 1), datetime(2027, 7, 31)), 2)

    def test_available_slots_outside_of_period(self):
        """Bookings outside of the period do not reduce the availability."""
        self._create_order(datetime(2026, 1, 1), datetime(2026, 2, 1))

        self.assertEqual(self._get_available_count(datetime(2027, 1, 1), datetime(2027, 7, 31)), 5)
