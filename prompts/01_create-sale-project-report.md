---
title: "Create Sale Project Report"
state: completed
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

The goal of this task is to create module that introduces a new report model in the projekt app, including views and translations. 

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

### Views

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

- The report should not be visible for all users. Create a technical group that has access to this view.


## Worklog

The module `sale_project_report` has been completed with the following changes:

- **Model**: Created `report/project_report.py` with `project.report` SQL view model. The model aggregates per project:
  - `planned_hours` from `sale.order.line` (service, hours UOM)
  - `allocated_hours` from `project.task`
  - `timesheet_hours` from `account.analytic.line`
  - `invoiced_hours` from `sale.order.line.qty_invoiced`
  - Ratio fields `allocated_planned`, `timesheet_allocated`, `timesheet_planned` with `group_operator="avg"`
- **Views**: Added search, pivot and graph views in `views/project_report_views.xml`.
- **Menu**: Added "Project Analysis" under `project > reporting`.
- **Security**: Created technical group `group_sale_project_report_user` and restricted menu / model access to this group. Added multi-company rule.
- **Translations**: Added `i18n/de_CH.po` with German translations for model, fields, views, menu and group.
- **Manifest**: Updated dependencies to `sale_timesheet` and registered data files.

The generated QWeb report backbone from `task generate-module-report` was removed in favor of an SQL analysis report matching the `sale.report` / `account.invoice.report` pattern.
