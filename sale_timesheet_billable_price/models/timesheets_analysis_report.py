# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class TimesheetsAnalysisReport(models.Model):
    _inherit = ["timesheets.analysis.report"]


    @property
    def _table_query(self):
        return """
            SELECT
                B.id AS id,
                B.name AS name,
                B.user_id AS user_id,
                B.project_id AS project_id,
                B.task_id AS task_id,
                B.parent_task_id AS parent_task_id,
                B.employee_id AS employee_id,
                B.manager_id AS manager_id,
                B.company_id AS company_id,
                B.department_id AS department_id,
                B.currency_id AS currency_id,
                B.date AS date,
                B.amount AS amount,
                B.unit_amount AS unit_amount,
                B.order_id AS order_id,
                B.so_line AS so_line,
                B.timesheet_invoice_type AS timesheet_invoice_type,
                B.timesheet_invoice_id AS timesheet_invoice_id,
                CASE
                    WHEN SOL.id IS NOT NULL AND SOL.price_unit = 0
                    THEN 0
                    ELSE B.timesheet_revenues
                END AS timesheet_revenues,
                (
                    CASE
                        WHEN SOL.id IS NOT NULL AND SOL.price_unit = 0
                        THEN 0
                        ELSE B.timesheet_revenues
                    END + B.amount
                ) AS margin,
                CASE
                    WHEN SOL.id IS NOT NULL AND SOL.price_unit = 0
                    THEN 0
                    ELSE B.billable_time
                END AS billable_time,
                (
                    B.unit_amount - CASE
                        WHEN SOL.id IS NOT NULL AND SOL.price_unit = 0
                        THEN 0
                        ELSE B.billable_time
                    END
                ) AS non_billable_time
            FROM (
                %s
            ) B
            LEFT JOIN sale_order_line SOL ON SOL.id = B.so_line
        """ % (super()._table_query)
