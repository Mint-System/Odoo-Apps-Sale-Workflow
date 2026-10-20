---
commit_ref:
title: "Select lot when splitting a line"
author: "Janik von Rotz <login@janikvonrotz.ch>"
state: cancelled
date_completed: YYYY-MM-DD
harness:
model:
input_tokens:
output_tokens:
---

# Select lot when splitting a line

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I want you to update the `sale_renting_line_period` module. There is a split line
functionality where a user can enter a qty and then this amount is splitted into a new
sale order line.

If lots are assigned to the line it simply slices the set. I want you to add a new
option to the split dialog. The user should be able to select the lots that should be
splitted to the new line.

The split function checks if diff qty is equal to the selected lots. If no lots are
entered then use the slice approach.

Once ready I will test the functionality.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
