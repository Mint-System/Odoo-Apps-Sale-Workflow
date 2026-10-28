---
commit_ref:
title: "Re-migrate and update sale order ref"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
harness:
model:
input_tokens:
output_tokens:
---

# Re-migrate and update sale order ref

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

This is about the module `sale_order_ref`. There are 3 topics.

### 1. The module has been updated on 17.0 re-migrate the module.

There is a guide that explains how this is done: https://wiki.mint-system.ch/prozesse-odoo-modul-migration/?h=prozesse+modul+#modul-migrieren

Do not run any prompts or commit anything. Do not create feature branch or PR.

### 2. Update search filter on sale order

Add `ref` to field `name` in `sale.view_sales_order_filter`.

### 3. Make `sale_renting_line_period` depend on `sale_order_ref` and update search filter.

Add `ref` to field `name` in `sale_renting.rental_order_view_search`.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.
