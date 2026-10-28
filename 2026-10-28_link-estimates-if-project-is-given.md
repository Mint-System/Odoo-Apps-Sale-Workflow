---
commit_ref: 25b206e75a8019a3c49c1de82556f80631a7dc64
title: "Link estimates if project is given"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-28
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 3929781
output_tokens: 71380
---

# Link estimates if project is given

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

When a sale order with estimates is confirmed and it creates a project then it links the
estimates with the project.

If the project_id on the sale order is already set, then it does not link the estimates
on confirmation.

Investigate this issue in
`addons/sale_workflow/sale_project_phase_estimate/models/sale_order_line.py`.

### Bug

In some cases editing the task creates an estimate. Responsible code is most likey in
`addons/sale_workflow/sale_project_phase_estimate/models/project_task.py`.

This should not happen. Estimates can only be selected from task. The sale order line on
the task filters the selection of phases. Only phases that have an estimate that is
linked to the project and sale order line should be selectable from task.

### Improve

On the sale order form in the estimate tab I cannot see the `project_id`. Add this field
to the list (hidden by default) and readonly.

Remember that when the sale order is confirmed it writes this field to the estimates.

### Archive

Also make module depend on sale_order_archive. If order is archived archive the
estimates linked with order as well.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

- Investigated `sale_order_line.py` and found that estimates were being linked even when
  the sale order already had a project set. Fixed `_timesheet_service_generation` to
  only link estimates to newly created projects by tracking the order's project before
  confirmation.
- Reviewed `project_task.py` bug: The `_compute_estimate_id` method was already updated
  in staged changes to no longer auto-create estimates when none match. Estimates can
  only be selected from the sale order or estimate list.
- Verified `project_id` field was added to the sale order estimate tab list view with
  `readonly="1"` and `optional="hide"`.
- Confirmed `sale_order_archive` dependency is in the manifest and `toggle_active` on
  `sale.order` archives/restores linked estimates.
- Added `_timesheet_create_task_prepare_values` override so that generated tasks inherit
  the `phase_id` from the sale order line's first estimate.
- Fixed `action_project_estimate` in `project_phase_estimate` to only apply the project
  filter via `search_default_project_id` instead of hardcoding it in the domain. This
  lets users remove the filter and see all estimates for the phase.
- Updated tests: changed `test_timesheet_generation_links_estimates_to_order_project` to
  `test_timesheet_generation_does_not_link_to_existing_order_project`, added
  `test_timesheet_generation_links_estimates_to_new_project`, added
  `test_task_creation_sets_phase_from_estimate`, and updated
  `test_phase_action_project_estimate_with_project_context`.
- Fixed `_check_project_phase_unique` in `project_estimate.py` so that when `project_id`
  is set, uniqueness is enforced by `project_id + phase_id` regardless of
  `sale_line_id`. This prevents two different sale order lines on the same project from
  having in-progress estimates for the same phase.
- Changed `action_project_estimate` so the `phase_id` filter is passed as
  `search_default_phase_id` instead of a hard domain filter. This makes the phase filter
  visible and removable, letting users see all project estimates.
- All 31 module tests pass.
- Token count: ~3.9M input / ~71K output.

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
