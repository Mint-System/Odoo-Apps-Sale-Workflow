---
title: "sale-project-report replace JS code"
author: "laurens kooijman <laurenskooijman@gmail.com>"
action: implement
state: completed
date_completed: 2025-01-24
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 36603
output_tokens: 10596
---

# sale-project-report replace JS code

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

In the previous task for the module sale_project_report (tmp/prompt-log/2026-11-02_adjustments-to-saleprojectreport.md) you created clickable numbers with javascript. I don't want any Javascript in my module, therefore I have another approach that I want you to implement.

By default, when I click on a number, a list view is shown. I would like to have a button on that list view that goes to the related project dashboard/project updates kanban view that is used now.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

- Removed `js_class="project_report_pivot"` and `js_class="project_report_graph"` from pivot and graph views, restoring the default Odoo click behavior that opens a list view.
- Deleted custom JS files `project_report_pivot_view.js` and `project_report_graph_view.js`.
- Removed the `web.assets_backend` asset bundle entries from `__manifest__.py`.
- Added a new tree view `project_report_view_list` for the `project.report` model, marked as read-only with `create="0" edit="0" delete="0"`.
- **Fix: Used `<tree>` instead of `<list>` for Odoo 17 compatibility** — the `<list>` tag was introduced in Odoo 18.
- Added a tree-view button `action_open_project_updates` that calls a new Python method on `project.report`, which opens the `project.project_update_all_action` action scoped to the record's `project_id` via `active_id` in context.
- Updated German translations for the new button label and action display name.
- Verified Python syntax, XML validity, and PO file format.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.
