# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProjectReport(models.Model):
    _name = "project.report"
    _description = "Project Analysis"
    _auto = False
    _order = "project_id"

    planned_hours = fields.Float(string="Planned Hours", readonly=True)
    allocated_hours = fields.Float(string="Allocated Hours", readonly=True)
    timesheet_hours = fields.Float(string="Timesheet Hours", readonly=True)
    invoiced_hours = fields.Float(string="Invoiced Hours", readonly=True)
    allocated_planned = fields.Float(
        string="Allocated / Planned", readonly=True, group_operator="avg"
    )
    timesheet_allocated = fields.Float(
        string="Timesheet / Allocated", readonly=True, group_operator="avg"
    )
    timesheet_planned = fields.Float(
        string="Timesheet / Planned", readonly=True, group_operator="avg"
    )
    project_id = fields.Many2one(
        comodel_name="project.project", string="Project", readonly=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Customer", readonly=True
    )
    user_id = fields.Many2one(
        comodel_name="res.users", string="Project Manager", readonly=True
    )
    company_id = fields.Many2one(
        comodel_name="res.company", string="Company", readonly=True
    )

    @property
    def _table_query(self):
        return f"""
            WITH planned AS (
                SELECT
                    sol.project_id,
                    SUM(sol.product_uom_qty) AS planned_hours
                FROM sale_order_line sol
                JOIN product_product pp ON pp.id = sol.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                JOIN uom_uom uom ON uom.id = sol.product_uom
                WHERE sol.display_type IS NULL
                    AND pt.type = 'service'
                    AND uom.id = {self.env.ref('uom.product_uom_hour').id}
                    AND sol.product_uom_qty > 0
                    AND sol.price_unit > 0
                    AND sol.project_id IS NOT NULL
                GROUP BY sol.project_id
            ),
            allocated AS (
                SELECT
                    pt.project_id,
                    SUM(pt.allocated_hours) AS allocated_hours
                FROM project_task pt
                JOIN sale_order_line sol ON sol.id = pt.sale_line_id
                WHERE pt.project_id IS NOT NULL
                    AND sol.price_unit > 0
                GROUP BY pt.project_id
            ),
            timesheet AS (
                SELECT
                    aal.project_id,
                    SUM(aal.unit_amount) AS timesheet_hours,
                    SUM(
                        CASE
                            WHEN aal.timesheet_invoice_id IS NOT NULL
                            THEN aal.unit_amount
                            ELSE 0
                        END
                    ) AS invoiced_hours
                FROM account_analytic_line aal
                JOIN sale_order_line sol ON sol.id = aal.so_line
                WHERE aal.project_id IS NOT NULL
                    AND sol.price_unit > 0
                GROUP BY aal.project_id
            )
            SELECT
                p.id AS id,
                p.id AS project_id,
                p.partner_id AS partner_id,
                p.user_id AS user_id,
                p.company_id AS company_id,
                COALESCE(planned.planned_hours, 0.0) AS planned_hours,
                COALESCE(allocated.allocated_hours, 0.0) AS allocated_hours,
                COALESCE(timesheet.timesheet_hours, 0.0) AS timesheet_hours,
                COALESCE(timesheet.invoiced_hours, 0.0) AS invoiced_hours,
                CASE
                    WHEN COALESCE(planned.planned_hours, 0) > 0
                    THEN COALESCE(allocated.allocated_hours, 0) / planned.planned_hours
                    ELSE 0
                END AS allocated_planned,
                CASE
                    WHEN COALESCE(allocated.allocated_hours, 0) > 0
                    THEN COALESCE(timesheet.timesheet_hours, 0) / allocated.allocated_hours
                    ELSE 0
                END AS timesheet_allocated,
                CASE
                    WHEN COALESCE(planned.planned_hours, 0) > 0
                    THEN COALESCE(timesheet.timesheet_hours, 0) / planned.planned_hours
                    ELSE 0
                END AS timesheet_planned
            FROM project_project p
            LEFT JOIN planned ON planned.project_id = p.id
            LEFT JOIN allocated ON allocated.project_id = p.id
            LEFT JOIN timesheet ON timesheet.project_id = p.id
            WHERE p.active = true
        """
