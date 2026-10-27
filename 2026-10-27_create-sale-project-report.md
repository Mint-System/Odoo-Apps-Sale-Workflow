---
commit_ref: 272c39a99a5f745419a981309444bcdc44f5c564
title: "Create Sale Project Report"
state: completed
date: 2026-10-23
model: moonshotai/Kimi-K2.6
input_tokens: 
output_tokens: 
---

# Run 01

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

The goal of this task is to create a module that introduces a new report model in the projekt app, including views and translations. 

The module has already been initialized and can be found in "addons/sale_workflow/sale_project_report"

### Report

- Create the backbone for the new report using `task generate-module-report addons/sale_workflow/sale_project_report project.report`
- Before filling the new report `project.report`, read the reports `sale.report` and `account.invoice.report`. The new report should be created in a similar way.
- These fields should be part of the report. In brackets is how the new fields should be calculated.
planned_hours / Geplante Stunden (sale.order.line:product_uom_qty with filter: uom is hours und type ist service und amount > 0)
allocated_hours / Freigebene Stunden (project.task:allocated_hours)
timesheet_hours / Zeiterfassungsstunden (account.analytic.line:unit_amount)
allocated_planned / Anteil freigebene von geplante Stunden (ratio allocated_hours/planned_hours - Make this field aggregate by average)
timesheet_allocated / Anteil Zeiterfassung von freigebene Stunden (ratio timesheet_hours/allocated_hours - Make this field aggregate by average)
timesheet_planned / Anteil Zeiterfassung von geplante Stunden (ratio timesheet_hours/planned_hours - Make this field aggregate by average)
project_id
partner_id
user_id
- If possible, add this field as well
invoiced_hours / Verrechnete Stunden

#### Views

Include the view file in report as is standard in other reports.

- Create a menu entry in "project > reporting > Project Analysis"
- Create search, pivot and graph view for the report with the values:
planned_hours
allocated_hours
timesheet_hours
allocated_planned
timesheet_allocated
timesheet_planned
invoiced_hours (if possible)

### Translations

- Add a translations file for "de_CH" with all parts inside this module that should be translated. Give your best estimation for translations.

### Rights

- The report should not be visible for all users. Only make it visible for the group "project/Administrator".

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

- Created `project.report` model (`report/project_report.py`) as an SQL-based analysis view (similar to `sale.report` and `account.invoice.report`) with the following measures:
  - `planned_hours`: sum of `sale.order.line.product_uom_qty` for service products with hours UOM and positive amount.
  - `allocated_hours`: sum of `project.task.allocated_hours`.
  - `timesheet_hours`: sum of `account.analytic.line.unit_amount`.
  - `invoiced_hours`: subset of timesheet hours linked to an invoice (`timesheet_invoice_id IS NOT NULL`).
  - `allocated_planned`, `timesheet_allocated`, `timesheet_planned`: computed ratios with `group_operator="avg"`.
  - Dimensions: `project_id`, `partner_id`, `user_id` (project manager), `company_id`.
- Added views (`report/project_report_views.xml`): search, pivot, graph, and an action opening graph+pivot.
- Added menu entry **Project Analysis** under *Project > Reporting* visible only to `project.group_project_manager`.
- Added security: read access restricted to `project/Administrator` via `ir.model.access.csv`, and a multi-company record rule.
- Added German (de_CH) translations in `i18n/de_CH.po`.
- Module registered in `__manifest__.py` and `__init__.py`.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.

## Follow-up changes

After initial completion the following adjustments were made:

- Wrote brief test instructions in `tests/TEST_INSTRUCTIONS.rst`.
- Changed the action `view_mode` from `graph,pivot` to `pivot,graph` so the pivot view opens first.
- Added `disable_linking="1"` to both pivot and graph views to prevent clickable numbers from opening an empty list view.
- Changed the `planned_hours` CTE filter from `price_subtotal > 0` to `price_unit > 0`.
- Extended the `price_unit > 0` filter to the `allocated_hours` and `timesheet_hours`/`invoiced_hours` CTEs by joining `sale_order_line` so that only billable tasks and timesheets are included.
