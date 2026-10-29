# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command

from odoo.addons.sale.tests.common import SaleCommon


class TestStockRentalSlotStockSync(SaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.printer = cls.env["product.product"].create(
            {
                "name": "Test Printer",
                "type": "consu",
                "is_storable": True,
                "tracking": "serial",
                "rent_ok": True,
            }
        )
        cls.lot = cls.env["stock.lot"].create(
            {
                "name": "PRINT001",
                "product_id": cls.printer.id,
            }
        )
        cls.location = cls.env.ref("stock.stock_location_stock")

    def test_placeholder_created_when_quant_added(self):
        """Placeholder slots must exist for storable rental lots regardless of quant state."""
        self.assertTrue(self.lot.start_slot_id)
        self.assertTrue(self.lot.start_slot_id.is_placeholder)

    def test_placeholder_removed_when_qty_zero(self):
        """Setting lot quantity to zero must remove the placeholder slot."""
        quant = self.env["stock.quant"].create(
            {
                "product_id": self.printer.id,
                "lot_id": self.lot.id,
                "location_id": self.location.id,
                "quantity": 1.0,
            }
        )
        self.assertTrue(self.lot.start_slot_id)
        quant.write({"quantity": 0.0})
        self.assertFalse(self.lot.start_slot_id)

    def test_placeholder_removed_when_quant_unlinked(self):
        """Unlinking the quant of a lot must remove the placeholder slot."""
        quant = self.env["stock.quant"].create(
            {
                "product_id": self.printer.id,
                "lot_id": self.lot.id,
                "location_id": self.location.id,
                "quantity": 1.0,
            }
        )
        self.assertTrue(self.lot.start_slot_id)
        quant.unlink()
        self.assertFalse(self.lot.start_slot_id)

    def test_placeholder_name_prefix(self):
        """Placeholder slot names must be prefixed with 'Placeholder'."""
        self.env["stock.quant"].create(
            {
                "product_id": self.printer.id,
                "lot_id": self.lot.id,
                "location_id": self.location.id,
                "quantity": 1.0,
            }
        )
        slot = self.lot.start_slot_id
        self.assertTrue(slot.name.startswith("Placeholder"))

    def test_salesman_has_full_access(self):
        """A salesman must have full CRUD access on stock.rental.slot."""
        salesman = self.env["res.users"].create(
            {
                "name": "Test Salesman",
                "login": "test_salesman",
                "group_ids": [Command.set([self.env.ref("sales_team.group_sale_salesman").id])],
            }
        )
        slot = self.env["stock.rental.slot"].create({"lot_id": self.lot.id, "product_id": self.printer.id})
        self.env["stock.rental.slot"].with_user(salesman).write({"lot_id": self.lot.id})
        self.env["stock.rental.slot"].with_user(salesman).unlink()
