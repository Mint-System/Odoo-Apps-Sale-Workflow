---
title: "Link estimates if project is given"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
harness:
model:
input_tokens:
output_tokens:
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

When a sale order with estimates is confirmed and it creates a project then it links the estimates with the project.

If the project_id on the sale order is already set, then it does not link the estimates on confirmation.

Investigate this issue in `addons/sale_workflow/sale_project_phase_estimate/models/sale_order_line.py`.

### Bug

In some cases editing the task creates an estimate. Responsible code is most likey in `addons/sale_workflow/sale_project_phase_estimate/models/project_task.py`.

This should not happen. Estimates can only be selected from task. The sale order line on the task filters the selection of phases. Only phases that have an estimate that is linked to the project and sale order line should be selectable from task.

### Improve

On the sale order form in the estimate tab I cannot see the `project_id`. Add this field to the list (hidden by default) and readonly.

Remember that when the sale order is confirmed it writes this field to the estimates.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.
