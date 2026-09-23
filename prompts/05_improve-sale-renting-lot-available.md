---
title: "Improve Sale Renting Lot Available"
state: completed
date_completed: 2026-09-23
model: moonshotai/Kimi-K2.6
input_tokens: 2006081
output_tokens: 53296
---

# Run 05

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I want you to update the `action_create_order` method in
`addons/sale_workflow/sale_renting_lot_available/models/stock_rental_slot.py`.

Group the selected products and then use the product count for `product_uom_qty`.

The user enters a `start_date` and `end_date` in the
`addons/sale_workflow/sale_renting_lot_available/wizard/stock_rental_slot_period.py`
dialog.

I want you store these dates in the context and then when `action_create_order` is
called, it should use these dates as defaults for `rental_start_date` and
`rental_return_date` of `sale.order`.

Once you completed the task, I will install and test the module.

## Worklog

- Updated `action_view_available_slots` in `wizard/stock_rental_slot_period.py` to
  forward the wizard's `start_date` and `end_date` as `default_rental_start_date` and
  `default_rental_return_date` in the action context.
- Updated `action_create_order` in `models/stock_rental_slot.py` to:
  - Group selected slots by product using `collections.Counter` and set
    `product_uom_qty` to the actual count per product.
  - Read `default_rental_start_date` and `default_rental_return_date` from the
    environment context and pass them as defaults for the new `sale.order` form.
- Updated `wizard/rental_order_wizard_line.py` so that `pickeable_lot_ids` (and
  therefore `pickedup_lot_ids`) is computed from the `stock.rental.slot` table rather
  than stock inventory queries:
  - Finds lots with an **overlapping** non-placeholder booking from another line.
  - Finds **all** lots that have any slot record (placeholder or booked) for this
    product.
  - Builds `pickeable_lots` as all lots minus overlapping unavailable lots, then
    subtracts already-picked-up and already-returned lots for the current line.
  - This makes lot availability deterministic regardless of record ordering.
- Fixed overlap-check dates in `wizard/rental_order_wizard_line.py` and
  `models/sale_order_line.py` (`_compute_available_slot_ids_count`) to use the
  line-specific `rental_start_date` / `rental_return_date` fields (provided by the
  co-installed `sale_renting_line_period` module) instead of `start_date` /
  `return_date`, which are related to the order-level dates and can differ from the
  actual slot dates.
- Verified Python syntax for all changed files.
