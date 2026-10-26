---
title: "Bugfix Sale Project Phase Estimate"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-26
harness: pi
model: moonshotai/Kimi-K2.6
---

# Bugfix Sale Project Phase Estimate

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

There is a bug in `sale_timesheet_estimate_report` please fix it.

### Bug: On task with phase with multiple estimates linked to different so_line, the estimates are not filtered by so_line

I want to set the same phase for so lines:

so1 - phase1 - 1h so2 - phase1 - 2h

But on the task if I have set phase1 and so1 then it should show progress based on h1.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

### Summary of Changes

Fixed the bug in `sale_project_phase_estimate` where task estimates were not filtered by
sale order line when multiple estimates shared the same phase.

1. **Overrode `_compute_estimate_id`**
   (`sale_project_phase_estimate/models/project_task.py`):

   - Added `sale_line_id` to the `@api.depends` decorator.
   - When `task.sale_line_id` is set, the estimate search domain now includes
     `("sale_line_id", "=", task.sale_line_id.id)`.
   - When creating a new estimate for a task with `sale_line_id`, the new estimate is
     created with `sale_line_id` populated.
   - Tasks without `sale_line_id` fall back to the original behavior.

2. **Created automated tests**
   (`sale_project_phase_estimate/tests/test_sale_project_phase_estimate.py` +
   `tests/__init__.py`):
   - 5 tests covering: filtering by sale line, fallback without sale line, creation with
     sale line, inverse phase setting sale line, and preserving existing sale line.

### Test Results

```
sale_project_phase_estimate: 5 tests 0.52s 369 queries
0 failed, 0 error(s) of 5 tests
```

---

Author confirmed results as completed.

---

## Update: Allow estimates with sale_line_id and no project_id

### Context

When creating quotes, the project does not exist yet. The `_check_project_phase_unique`
constraint from `project_phase_estimate` must be overridden to allow estimates with
`sale_line_id` but no `project_id`.

### Task

Overwrite `_check_project_phase_unique` in `sale_project_phase_estimate` to enforce:

- Unique by `(phase_id, is_in_progress, sale_line_id)` when `sale_line_id` is set.
- Unique by `(project_id, phase_id, is_in_progress)` when only `project_id` is set (no `sale_line_id`).

### Summary of Changes

1. **Overrode `_check_project_phase_unique`**
   (`sale_project_phase_estimate/models/project_estimate.py`):

   - When `sale_line_id` is set: checks for duplicates by
     `(phase_id, is_in_progress, sale_line_id)`.
   - When only `project_id` is set (no `sale_line_id`): checks for duplicates by
     `(project_id, phase_id, is_in_progress)`.
   - Estimates without `phase_id`, `is_in_progress`, or both identifiers are skipped.

2. **Updated automated tests**
   (`sale_project_phase_estimate/tests/test_sale_project_phase_estimate.py`):

   - `test_estimate_sale_line_without_project_allowed` — different `sale_line_id`s with
     the same phase and no project are allowed.
   - `test_estimate_sale_line_phase_unique_constraint` — duplicate `sale_line_id` with
     the same phase raises an error.

### Test Results

```
project_phase_estimate: 21 tests 0.60s 485 queries
sale_project_phase_estimate: 9 tests 0.40s 541 queries
0 failed, 0 error(s) of 26 tests
```
