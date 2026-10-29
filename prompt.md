---
title: "rental slots for storable products without tracking"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
harness:
model:
input_tokens:
output_tokens:
---

# rental slots for storable products without tracking

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

This is aobut `addons/sale_workflow/sale_renting_lot_available`.

There are currently three ways how rental slots are created or updated:

- A `stock.lot` is created -> `_create_stock_rental_lot` -> creates placeholder slots
- A `sale.order.line` is created -> `_generate_stock_rental_lot` -> creates booking slots
- A `stock.quant` is updated -> `_generate_stock_rental_lot` -> re-recretates the placeholder slots of the lot

I want you to add two new ways to genrate placeholder slots:

- A `qty_available` on a product with `rent_ok`, `is_storable` and `tracking=='none'` is set -> `_generate_stock_rental_lot` -> delete linked slots and create one for each qty
- Set qty on a `stock.quant` for a product with `rent_ok`, `is_storable` and `tracking=='none'` is set ->  `_generate_stock_rental_lot` -> delete linked slots and create one for each qty

The name of these slots becomes "Placeholder - {Product}".

### Slot and product link

This will require an update on `stock.rental.slot`. The `product_id` must no longer be computed from `lot_id` or `so_line_id`. Instead make this a readonly field and set the `product_id` in the `_create_stock_rental_lot` and `_generate_stock_rental_lot` methods.

### Demo data

Create a demo rental product that matches the new conditions.

### Testing

Write tests for the functionality.

Prepare the Odoo enviroment for testing.

I will test if the rental flow still works.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.
