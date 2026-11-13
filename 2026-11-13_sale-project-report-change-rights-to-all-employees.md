---
commit_ref: 64b1667b686ac509266f274e7941d12b1ac37e2b
title: "sale project report change rights to all employees"
author: "laurens kooijman <laurenskooijman@gmail.com>"
action: implement
state: completed
date_completed: 2026-11-13
harness: pi
provider: infomaniak
model: moonshotai/Kimi-K2.6
input_tokens: 29296
output_tokens: 2379
---

# sale project report change rights to all employees

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

In the module `sale_project_report`, the created report is set to only be visible by project administrators (`project.group_project_manager`. I want you to change this so that the report is visible and accessible for the project users (group `project.group_project_user`. 

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

- Changed the menuitem `groups` attribute in `sale_project_report/report/project_report_views.xml` from `project.group_project_manager` to `project.group_project_user`.
- Updated the access rule in `sale_project_report/security/ir.model.access.csv` to grant read access to `project.group_project_user` instead of `project.group_project_manager`.

This makes the Project Analysis report visible and accessible to all project users, not just project managers.

Please verify that project users can now see the **Project Analysis** menu item under the Project reporting section and can open the report without access errors.

If results are confirmed, set frontmatter state to `completed` and add today's date to `date_completed`. If not, set to `aborted`.
