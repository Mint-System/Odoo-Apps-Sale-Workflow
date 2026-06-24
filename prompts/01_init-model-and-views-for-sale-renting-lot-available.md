---
title: "Init model and views for sale renting lot available"
state: completed
---

# Run 01

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I want you to create a new model `stock.lot.rental` and `stock.lot.rental.period` in
`addons/sale_workflow/sale_renting_lot_available`. Use
`task generate-module-model addons/sale_workflow/sale_renting_lot_available <model>` to
generate the files.

For `stock.lot.rental` create these fields:

| Label           | Name          | Typ                       | Description                               |
| --------------- | ------------- | ------------------------- | ----------------------------------------- |
| Lot             | lot_id        | many2one stock.lot        |                                           |
| Product         | product_id    | many2one product.product  | Linked with lot_id.product_id             |
| Category        | cateq_id      | many2one product.category | Linked with product_id.cateq_id           |
| Sale Order Line | so_line_id    | many2one sale.order.line  |                                           |
| Rental Status   | rental_status | selection                 | Linked with so_line_id.rental_status      |
| Is Late         | is_late       | boolean                   | Linked with so_line_id.                   |
| Sale Order      | sale_order_id | many2one sale.order       | Linked with so_line_id.order_id           |
| Start Date      | start_date    | datetime                  | Linked with so_line_id.rental_start_date  |
| Return Date     | return_date   | datetime                  | Linked with so_line_id.rental_return_date |

For `stock.lot.rental.period` create these fields:

| Label       | Name        | Typ      | Description          |
| ----------- | ----------- | -------- | -------------------- |
| Start Date  | start_date  | datetime | Start date of rental |
| Return Date | return_date | datetime | Start date of rental |

Add model security with
`task generate-module-security addons/sale_workflow/sale_renting_lot_available <model>`.

Then for `stock.lot.renal` I want you to setup views. Use
`task generate-module-views addons/sale_workflow/sale_renting_lot_available <model>` to
do so. Remove the generate menu entries. Replace the action for the existing
`sale_renting.menu_rental_schedule` menu.

Once everything is ready I will install and test the module.

## Worklog

@Clanker Add a summary here once the task has been completed.

Created `stock.lot.rental` and `stock.lot.rental.period` models with the specified
fields. Used `task generate-module-model` and `task generate-module-security` to
scaffold files. Defined related fields on `stock.lot.rental` to pull values from the
linked `sale.order.line` (`rental_status`, `is_late`, `order_id`, `rental_start_date`,
`rental_return_date`) and `stock.lot` (`product_id`, `categ_id`). Added
`_rec_name = "lot_id"` on `stock.lot.rental` for display naming.

Generated views with `task generate-module-views`, then replaced the generated menu
entries with a single record override that updates
`sale_renting.menu_rental_schedule.action` to point to the new
`action_stock_lot_rental_view`. The form, list, and search views expose all relevant
rental lot fields and include useful filters (Late, group by Category/Status/Sale
Order).

Updated the manifest to reference `security/ir.model.access.csv` and
`views/stock_lot_rental_views.xml`. All pre-commit checks pass for the modified files.

@Clanker Set frontmatter state to completed.
