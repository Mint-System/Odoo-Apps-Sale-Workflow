# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestSaleProjectPhaseEstimate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.project = cls.env["project.project"].create(
            {
                "name": "Test Project",
                "partner_id": cls.partner.id,
            }
        )
        cls.phase = cls.env["project.task.phase"].create({"name": "Test Phase"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Service",
                "type": "service",
                "service_tracking": "task_global_project",
                "project_id": cls.project.id,
            }
        )
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
            }
        )
        cls.so_line_1 = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.product.id,
                "product_uom_qty": 1,
            }
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Test Task",
                "project_id": cls.project.id,
                "sale_line_id": cls.so_line_1.id,
                "phase_id": cls.phase.id,
            }
        )

    def test_task_estimate_id_matches_sale_line(self):
        """Task estimate_id should link to estimate matching phase, project, and sale_line."""
        # There is already an auto-created estimate from task creation
        self.task.estimate_id.sale_line_id = self.so_line_1
        self.task._compute_estimate_id()
        self.assertEqual(self.task.estimate_id.sale_line_id, self.so_line_1)

    def test_task_estimate_id_creates_with_sale_line(self):
        """Task with sale_line but no matching estimate should create one with sale_line."""
        # Remove existing auto-created estimate to force creation
        existing = self.env["project.estimate"].search(
            [
                ("project_id", "=", self.project.id),
                ("phase_id", "=", self.phase.id),
            ]
        )
        existing.unlink()
        self.assertFalse(
            self.env["project.estimate"].search(
                [
                    ("project_id", "=", self.project.id),
                    ("phase_id", "=", self.phase.id),
                ]
            )
        )
        self.task._compute_estimate_id()
        estimate = self.task.estimate_id
        self.assertTrue(estimate)
        self.assertEqual(estimate.sale_line_id, self.so_line_1)

    def test_inverse_phase_id_sets_sale_line(self):
        """Setting phase_id on a task without sale_line should set sale_line from estimate."""
        phase2 = self.env["project.task.phase"].create({"name": "Other Phase"})
        task = self.env["project.task"].create(
            {
                "name": "Task without SO line",
                "project_id": self.project.id,
            }
        )
        self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": phase2.id,
                "sale_line_id": self.so_line_1.id,
                "planned_hours": 3.0,
            }
        )
        task.phase_id = phase2
        self.assertEqual(task.sale_line_id, self.so_line_1)

    def test_inverse_phase_id_does_not_overwrite_existing_sale_line(self):
        """Setting phase_id should not overwrite an existing sale_line."""
        phase2 = self.env["project.task.phase"].create({"name": "Another Phase"})
        self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": phase2.id,
                "sale_line_id": self.so_line_1.id,
                "planned_hours": 4.0,
            }
        )
        existing_sale_line = self.task.sale_line_id
        self.task.phase_id = phase2
        self.assertEqual(self.task.sale_line_id, existing_sale_line)

    def test_estimate_project_phase_unique_constraint(self):
        """Creating two estimates with the same project and phase should raise an error."""
        phase3 = self.env["project.task.phase"].create({"name": "Unique Phase"})
        self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": phase3.id,
                "planned_hours": 10,
            }
        )
        with self.assertRaises(Exception):
            self.env["project.estimate"].create(
                {
                    "project_id": self.project.id,
                    "phase_id": phase3.id,
                    "planned_hours": 20,
                }
            )

    def test_estimate_sale_line_without_project_allowed(self):
        """Different sale_line_id with same phase and no project should be allowed."""
        so_line_2 = self.env["sale.order.line"].create(
            {
                "order_id": self.sale_order.id,
                "product_id": self.product.id,
                "product_uom_qty": 1,
            }
        )
        self.env["project.estimate"].create(
            {
                "phase_id": self.phase.id,
                "sale_line_id": self.so_line_1.id,
                "planned_hours": 10,
            }
        )
        # Same phase, different sale line, no project: should be allowed
        self.env["project.estimate"].create(
            {
                "phase_id": self.phase.id,
                "sale_line_id": so_line_2.id,
                "planned_hours": 20,
            }
        )
        # Verify both exist
        estimates = self.env["project.estimate"].search(
            [
                ("phase_id", "=", self.phase.id),
                ("project_id", "=", False),
            ]
        )
        self.assertEqual(len(estimates), 2)

    def test_estimate_sale_line_phase_unique_constraint(self):
        """Duplicate sale_line_id with same phase should raise an error."""
        self.env["project.estimate"].create(
            {
                "phase_id": self.phase.id,
                "sale_line_id": self.so_line_1.id,
                "planned_hours": 10,
            }
        )
        with self.assertRaises(Exception):
            self.env["project.estimate"].create(
                {
                    "phase_id": self.phase.id,
                    "sale_line_id": self.so_line_1.id,
                    "planned_hours": 20,
                }
            )
