---
title: "smart button for lot"
state: completed
model: infomaniak/moonshotai/Kimi-K2.6
input_tokens: ~4000
output_tokens: ~3000
---

# Run 04

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I have added a smart button to
`addons/sale_workflow/sale_renting_lot_available/views/sale_order_views.xml`.

Can you do the same for `stock.lot` in
`addons/sale_workflow/sale_renting_lot_available/views/stock_lot_views.xml`?

Of course this requires adding new fields to the `stock.lot` model.

## Worklog

Added a smart button to `stock.lot` form view, mirroring the existing `sale.order`
implementation.

Changes made:

- `models/stock_lot.py`: Added `rental_slot_count` (Integer, computed) field and
  `action_view_rental_slots` method that opens the `stock.rental.slot` gantt/list/form
  view filtered for the current lot.
- `views/stock_lot_views.xml`: Added an inherited view record that injects a
  `oe_stat_button` into the `button_box` of `stock.view_production_lot_form`. The button
  is hidden when `rental_slot_count == 0`, uses the `fa-calendar` icon, and displays the
  count via `statinfo` widget.

@Clanker Set frontmatter state to completed and update info about model and token usage.
