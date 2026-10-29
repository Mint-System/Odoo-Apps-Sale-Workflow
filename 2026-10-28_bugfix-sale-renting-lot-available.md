---
commit_ref: 34a666c1b383aef8bb9b71dab27e868f3f7b2685
title: "Bugfix Sale Renting Lot Available"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-29
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens:
output_tokens:
---

# Bugfix Sale Rening Lot Available

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

This about module `sale_renting_lot_available`.

### User access to `stock.rental.slot`

Ensure that users in group `sales_team.group_sale_salesman` have full access on the slot
model.

### Lot 0 does not remove placeholder slot

If qty for a `stock.lot` is set to 0.0 it should remove the placeholder slots.

### Placeholder slots with prefix in name

Ensure that if `is_placeholder` is set then the name is prefixed with "Placeholder".

So the name becomes "Placeholder - {Product} - {Lot}".

### Testing

Prepare the Odoo environment for testing.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

### Summary

1. **User access to `stock.rental.slot`**: Added access rules in
   `security/ir.model.access.csv` granting `sales_team.group_sale_salesman` full CRUD
   permissions on `model_stock_rental_slot` and `model_stock_rental_slot_period`.

2. **Lot 0 removes placeholder slot**: Created `models/stock_quant.py` to sync
   placeholder slots with lot quantity changes. When a `stock.quant` is created,
   updated, or unlinked for a storable rental product, the code checks whether the
   related lot's `product_qty` dropped to `0.0` and removes the placeholder slot
   accordingly. It also recreates the placeholder if stock is restored.

3. **Placeholder slots with prefix in name**: Updated `_compute_name` in
   `models/stock_rental_slot.py` to prefix placeholder slot names with "Placeholder - ".

4. **Testing**: Prepared the Odoo environment (started DB `19.0`, initialized and
   installed module). Added `tests/test_slot_stock_sync.py` covering placeholder removal
   on quantity zero, placeholder removal on quant unlink, placeholder name prefix, and
   salesman access. All tests pass (8/8).

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
