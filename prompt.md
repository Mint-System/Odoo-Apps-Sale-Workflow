---
title: "Split for each qty"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
harness:
model:
input_tokens:
output_tokens:
---

# Split for each qty

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

### Split action

The `action_split_line` method in `addons/sale_workflow/sale_renting_line_period` shows a dialog where the user can enter the amount to split. Instead of this entry I wanto the method to split the one line into lines for each qty. The dialog should simply give a warning about what is going to happen.

### Bug compute rental sate

This bug concerns `sale_renting_line_period`.

Then there is a bug in `sale.order.line:_compute_rental_status`. When the lines were picked up and then splitted, the new line would be in state `returned` instead of `return`.

Double check this issue. Maybe it is resolved with the new split line function.

### Bug qty > delivered missing slots

This bug concerns `sale_renting_lot_available`.

If only a partial amount for a sale order line is delivered the slots are regenerated.

If qty is 4 and delivered is 3 then it generates only 3 slots instead of 4. This is probably because it generates slots for pickedup_lot_ids only.

But the it should slots for pickedup_lot_ids + 4-3=1 qty in this case.

### Support multi company

This enahncement concerns `sale_renting_lot_available`.

I would like to have multi-company support for slots. Add a `company_id` field to the `stock.rental.slot`.

### Testing

There are test instructions for each module.

I am asking you to create a simple actual test for both modules.

For `sale_renting_line_period` simply test the split function.

For `sale_renting_lot_available` simply check the slot generation function.

Do not cover all test from test instructions.

I will also do manuall test.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.
