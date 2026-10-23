# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class ProjectReport(models.Model):
    _name = "project.report"
    _description = "Project Analysis Report"
    _auto = False
    _order = "project_id"

    project_id = fields.Many2one("project.project", string="Project", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Customer", readonly=True)
    user_id = fields.Many2one("res.users", string="Project Manager", readonly=True)
    company_id = fields.Many2one("res.company", string="Company", readonly=True)
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

    def _select(self):
        return """
            SELECT
                pp.id AS id,
                pp.id AS project_id,
                pp.partner_id,
                pp.user_id,
                pp.company_id,
                COALESCE(planned.planned_hours, 0.0) AS planned_hours,
                COALESCE(allocated.allocated_hours, 0.0) AS allocated_hours,
                COALESCE(timesheet.timesheet_hours, 0.0) AS timesheet_hours,
                COALESCE(invoiced.invoiced_hours, 0.0) AS invoiced_hours,
                CASE
                    WHEN COALESCE(planned.planned_hours, 0.0) > 0
                    THEN COALESCE(allocated.allocated_hours, 0.0) / planned.planned_hours
                    ELSE 0.0
                END AS allocated_planned,
                CASE
                    WHEN COALESCE(allocated.allocated_hours, 0.0) > 0
                    THEN COALESCE(timesheet.timesheet_hours, 0.0) / allocated.allocated_hours
                    ELSE 0.0
                END AS timesheet_allocated,
                CASE
                    WHEN COALESCE(planned.planned_hours, 0.0) > 0
                    THEN COALESCE(timesheet.timesheet_hours, 0.0) / planned.planned_hours
                    ELSE 0.0
                END AS timesheet_planned
        """

    def _from(self):
        return """
            FROM project_project pp
            LEFT JOIN (
                SELECT sol.project_id,
                       SUM(sol.product_uom_qty) AS planned_hours
                  FROM sale_order_line sol
                  JOIN product_product pp2 ON pp2.id = sol.product_id
                  JOIN product_template pt ON pt.id = pp2.product_tmpl_id
                  JOIN uom_uom u ON u.id = sol.product_uom
                 WHERE pt.type = 'service'
                   AND u.id = (
                       SELECT res_id
                         FROM ir_model_data
                        WHERE module = 'uom'
                          AND name = 'product_uom_hour'
                   )
                   AND sol.product_uom_qty > 0
                   AND sol.display_type IS NULL
                 GROUP BY sol.project_id
            ) planned ON planned.project_id = pp.id
            LEFT JOIN (
                SELECT pt.project_id,
                       SUM(pt.allocated_hours) AS allocated_hours
                  FROM project_task pt
                 WHERE pt.project_id IS NOT NULL
                 GROUP BY pt.project_id
            ) allocated ON allocated.project_id = pp.id
            LEFT JOIN (
                SELECT aal.project_id,
                       SUM(aal.unit_amount) AS timesheet_hours
                  FROM account_analytic_line aal
                 WHERE aal.project_id IS NOT NULL
                   AND aal.unit_amount > 0
                 GROUP BY aal.project_id
            ) timesheet ON timesheet.project_id = pp.id
            LEFT JOIN (
                SELECT sol.project_id,
                       SUM(sol.qty_invoiced) AS invoiced_hours
                  FROM sale_order_line sol
                  JOIN product_product pp2 ON pp2.id = sol.product_id
                  JOIN product_template pt ON pt.id = pp2.product_tmpl_id
                  JOIN uom_uom u ON u.id = sol.product_uom
                 WHERE pt.type = 'service'
                   AND u.id = (
                       SELECT res_id
                         FROM ir_model_data
                        WHERE module = 'uom'
                          AND name = 'product_uom_hour'
                   )
                   AND sol.qty_invoiced > 0
                   AND sol.display_type IS NULL
                 GROUP BY sol.project_id
            ) invoiced ON invoiced.project_id = pp.id
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS
            {self._select()}
            {self._from()}
        """)
