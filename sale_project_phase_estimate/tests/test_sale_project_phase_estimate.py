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
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "sale_line_id": self.so_line_1.id,
                "planned_hours": 5.0,
            }
        )
        self.task._compute_estimate_id()
        self.assertEqual(self.task.estimate_id, estimate)

    def test_task_estimate_id_does_not_create(self):
        """Task estimate_id must not create an estimate when none matches."""
        self.assertFalse(self.task.estimate_id)
        self.task._compute_estimate_id()
        self.assertFalse(self.task.estimate_id)
        estimate = self.env["project.estimate"].search(
            [
                ("project_id", "=", self.project.id),
                ("phase_id", "=", self.phase.id),
            ]
        )
        self.assertFalse(estimate)

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

    def test_estimate_project_phase_unique_with_different_sale_lines(self):
        """Same project and phase with different sale lines should raise an error."""
        so_line_2 = self.env["sale.order.line"].create(
            {
                "order_id": self.sale_order.id,
                "product_id": self.product.id,
                "product_uom_qty": 1,
            }
        )
        self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "sale_line_id": self.so_line_1.id,
                "planned_hours": 10,
            }
        )
        with self.assertRaises(Exception):
            self.env["project.estimate"].create(
                {
                    "project_id": self.project.id,
                    "phase_id": self.phase.id,
                    "sale_line_id": so_line_2.id,
                    "planned_hours": 20,
                }
            )

    def test_timesheet_generation_does_not_link_to_existing_order_project(self):
        """Estimates are not linked when the order already had a project."""
        estimate = self.env["project.estimate"].create(
            {
                "phase_id": self.phase.id,
                "sale_line_id": self.so_line_1.id,
                "planned_hours": 2.0,
            }
        )
        self.sale_order.project_id = self.project
        self.so_line_1._timesheet_service_generation()
        self.assertFalse(estimate.project_id)

    def test_timesheet_generation_links_estimates_to_new_project(self):
        """Estimates are linked to a newly created project during confirmation."""
        product_project = self.env["product.product"].create(
            {
                "name": "Project Service",
                "type": "service",
                "service_tracking": "project_only",
            }
        )
        so_line = self.env["sale.order.line"].create(
            {
                "order_id": self.sale_order.id,
                "product_id": product_project.id,
                "product_uom_qty": 1,
            }
        )
        estimate = self.env["project.estimate"].create(
            {
                "phase_id": self.phase.id,
                "sale_line_id": so_line.id,
                "planned_hours": 2.0,
            }
        )
        so_line._timesheet_service_generation()
        self.assertTrue(estimate.project_id)

    def test_task_creation_sets_phase_from_estimate(self):
        """Generated task should inherit the phase from the sale line's estimate."""
        product_task = self.env["product.product"].create(
            {
                "name": "Task Service",
                "type": "service",
                "service_tracking": "task_global_project",
                "project_id": self.project.id,
            }
        )
        so_line = self.env["sale.order.line"].create(
            {
                "order_id": self.sale_order.id,
                "product_id": product_task.id,
                "product_uom_qty": 1,
            }
        )
        self.env["project.estimate"].create(
            {
                "phase_id": self.phase.id,
                "sale_line_id": so_line.id,
                "planned_hours": 2.0,
            }
        )
        task = so_line._timesheet_create_task(self.project)
        self.assertEqual(task.phase_id, self.phase)

    def test_toggle_active_archives_estimates(self):
        """Archiving the sale order archives the linked estimates as well."""
        estimate = self.env["project.estimate"].create(
            {
                "project_id": self.project.id,
                "phase_id": self.phase.id,
                "sale_line_id": self.so_line_1.id,
                "planned_hours": 2.0,
            }
        )
        self.assertTrue(estimate.active)
        self.sale_order.state = "done"
        self.sale_order.toggle_active()
        self.assertFalse(self.sale_order.active)
        self.assertFalse(estimate.active)
        self.sale_order.toggle_active()
        self.assertTrue(self.sale_order.active)
        self.assertTrue(estimate.active)
