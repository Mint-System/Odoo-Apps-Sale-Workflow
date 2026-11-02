---
title: "adjustments to sale_project_report"
author: "laurens kooijman <laurenskooijman@gmail.com>"
action: implement
state: completed
date_completed: 2025-01-24
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens:
output_tokens:
---

# adjustments to sale_project_report

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

In `sale_project_report` you created a module. Read the prompt that was used to create the module to understand the context. This prompt is stored here `tmp/prompt-log/2026-10-27_create-sale-project-report.md`.

I want to make some adjustments to the module.

- The fields `allocated_planned`, `timesheet_allocated`, `timesheet_planned` should be shown in the pivot table as percentages.

- In the Creation prompt I asked you to remove the possibility to click on the numbers in the pivot table. I want you to restore this feature and adjust the target of the clicks. Clicking on an number should go to the project update of the corresponding Project of that line. As a hint which view should be taken: in german this is the model "Projektaktualisierung" and the external id is project.project_update_view_kanban.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

- Added `widget="percentage"` to the ratio fields `allocated_planned`, `timesheet_allocated`, and `timesheet_planned` in both pivot and graph views so they display as percentages.
- Removed `disable_linking="1"` from the pivot and graph views to restore cell clickability.
- Introduced custom JS view classes (`project_report_pivot` and `project_report_graph`) with overridden click handlers that extract the `project_id` from the clicked cell's domain and redirect to the `project.update` kanban view filtered by that project.
- Registered the new JS files in the `web.assets_backend` bundle via `__manifest__.py`.
- Restored `disable_linking` removal — since the report model is a read-only SQL view, a fallback to the default list view occurs only when `project_id` cannot be determined from the clicked group.

- Changed the percentage ratio fields (`allocated_planned`, `timesheet_allocated`, `timesheet_planned`) to display without decimal places by adding `digits=(0, 0)` in the report model.
- Updated the custom pivot and graph click handlers to call the server-side action `project.project_update_all_action` with `additionalContext: { active_id: projectId }` instead of directly opening an act_window action. This opens Odoo's native project-updates kanban view (using the same action as the project-dashboard link) scoped to the clicked project.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.
