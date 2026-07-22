---
title: "implement new sale renting features"
state: completed
model: moonshotai/Kimi-K2.6
input_tokens:
---

# Run 03

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

**Create sale order from slot**

In `addons/sale_workflow/sale_renting_lot_available/views/stock_rental_slot_views.xml` I
have defined `action_create_order`. Implement this method.

I should create a new sale order and add a sale order line with qty 1 and the product_id
of self (sale.stock.slot).

I also want to be able to mark one or multiple slot in the list view and then run the
same action. For each unique product of slots a sale order line is added to the sale
order.

**Show gantt or list view**

When showing the wizard
`addons/sale_workflow/sale_renting_lot_available/wizard/stock_rental_slot_period.xml`
the user should be able to show results in gantt or in list view.

Add two button "View Gantt" and "View List" and pass the view mode to `action_apply`.
Rename `action_apply` to `action_view_gantt_or_list`.

Then I want you pass the default filters and groups in context:

- `lot_is_available`
- `groupby_product`
- `groupby_lot`

**Show Order button**

In the form view
`addons/sale_workflow/sale_renting_lot_available/views/stock_rental_slot_views.xml` I
would like to have an additional button `action_view_order`. If the slot is linked with
`sale_order_id` the `action_create_order` is hidden and the `action_view_order` is
shown.

## Worklog

- Implemented `action_create_order` in `models/stock_rental_slot.py` to open a blank
  `sale.order` form pre-filled with defaults. It passes `default_partner_id` (current
  user's partner), `default_order_line` (one line per unique product, qty 1),
  `link_rental_slot_ids` (selected slot IDs), and `in_rental_app: 1` via context. The
  order is only created when the user saves the form.
- Implemented `action_view_order` to open the linked `sale.order` form view when a slot
  has a `sale_order_id`.
- Updated `views/stock_rental_slot_views.xml` form view to conditionally show
  `action_create_order` (renamed button string to "Create Renting Order") when the slot
  has no order, and `action_view_order` when it has one.
- Renamed `action_apply` to `action_view_gantt_or_list` in
  `wizard/stock_rental_slot_period.py`, added dynamic `view_mode` support (gantt/list),
  fixed the domain to show slots **outside** the selected date range, and included
  default group-by context keys: `search_default_groupby_product` and
  `search_default_groupby_lot`.
- Updated `wizard/stock_rental_slot_period.xml` to replace the single "Apply" button
  with "View Gantt" and "View List" buttons, passing the respective `view_mode` via
  context.
- Created `models/sale_order.py` inheriting `sale.order`. Overrides `create` to read
  `link_rental_slot_ids` from context, matches new order lines to slots by product,
  unlinks auto-created rental slots, and links the original slots to the new lines.
- Added a smart button on `sale.view_order_form` via `views/sale_order_views.xml`. The
  button shows the count of linked rental slots and opens the rental slot gantt/list
  view with a context default filter on `sale_order_id` rather than a hard domain.
- Added `<field name="sale_order_id" />` to the `stock_rental_slot_search_view`.

@Clanker Set frontmatter state to completed and update info about model and token usage.
