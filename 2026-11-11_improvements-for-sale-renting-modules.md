---
commit_ref:
title: "Improvements for sale renting modules"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
harness:
provider:
model:
input_tokens:
output_tokens:
---

# Improvements for sale renting modules

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

I want you to improve the `sale_renting_line_period` and `sale_renting_lot_available` modules.

### Rental return datetime

The rental return datetime field must always set `23:59:59` (max time) as default time.

I was not possible to change the field to date type. So this is a workaround.

Update the `_compute_rental_period` method.

### Split sale order line not working

When I have a rental order with a deliverd line and want to split it, I get this error message:

> Die bestellte Menge einer Verkaufsauftragszeile kann nicht unter die bereits gelieferte Menge gesetzt werden. Legen Sie stattdessen eine Retoure in Ihrem Bestand an.

Try to reproduce this issue:

- reserved_lot_ids: set 8 lots
- pickedup_lot_ids: set 8 lots
- returned_lot_ids: 0
- product_uom_qty: 8
- qty_deliverd: 8
- qty_returned: 0 

My assumption is that `split()` in `addons/sale_workflow/sale_renting_line_period/wizard/rental_order_line_wizard.py` needs a fix.

### Check availability with non overlapping slots

The `get_available_slot_ids` in `addons/sale_workflow/sale_renting_lot_available/wizard/stock_rental_slot_period.py`  basically gets the non-placeholder slots that touch the boundaries of `end_date`  and `start_date`, counts them and returns count of placeholder slots minus the counted non-placeholder slots.

Now there is a problem with this simple approach. Assume with this setup:

We have a product with:

- placeholder slots: 5

Then we slot 1:

- start_date: 2026-12-01
- end_date: 2027-02-01

Then we slot 2:

- start_date: 2026-12-01
- end_date: 2027-08-31

Then we slot 3:

- start_date:  2027-07-01
- end_date: 2027-08-31

And then we check this date:

- start_date: 2027-01-01
- end_date: 2027-07-31

With the current setup the result of available slots is 5 - 3 = 2. Because all of the slots touch the boundaries.

But the correct result is 5 - 2 = 3. Because slot 3 starts after slot 2 ends. So these slots do not overlap.

I think soliving this issue requires a more sophisticated check. I think I need to know which slots do overlap in the time range which do not.

An new formular got get the available slots could be: placeholder sots - slots in boundaries + amount of slot pairs that do not overlap.

Instead of implementing this righ away please provide an approach on how to solve this problem.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness, provider and model. If you have access to session info also add token count. Finally, update the changelog with the most important changes.
