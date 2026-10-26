---
title: "Bugfix Sale Project Phase Estimate"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-26
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 6165921
output_tokens: 68273
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
