---
title: "rental slots for storable products without tracking"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-29T21:19:02+01:00
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 5601796
output_tokens: 38555
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
- A `sale.order.line` is created -> `_generate_stock_rental_lot` -> creates booking
  slots
- A `stock.quant` is updated -> `_generate_stock_rental_lot` -> re-recretates the
  placeholder slots of the lot

I want you to add two new ways to genrate placeholder slots:

- A `qty_available` on a product with `rent_ok`, `is_storable` and `tracking=='none'` is
  set -> `_generate_stock_rental_lot` -> delete linked slots and create one for each qty
- Set qty on a `stock.quant` for a product with `rent_ok`, `is_storable` and
  `tracking=='none'` is set -> `_generate_stock_rental_lot` -> delete linked slots and
  create one for each qty

The name of these slots becomes "Placeholder - {Product}".

### Slot and product link

This will require an update on `stock.rental.slot`. The `product_id` must no longer be
computed from `lot_id` or `so_line_id`. Instead make this a readonly field and set the
`product_id` in the `_create_stock_rental_lot` and `_generate_stock_rental_lot` methods.

### Demo data

Create a demo rental product that matches the new conditions.

### Testing

~~Write tests for the functionality.~~ Skip for now.

Prepare the Odoo enviroment for testing.

I will test if the rental flow still works.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

- Updated `stock.rental.slot` model: Changed `product_id` from computed to readonly
  field, removed `_compute_product_id`, updated `_compute_is_placeholder` to work
  without `lot_id`, updated `_compute_company_id` to use `product_id.company_id`, and
  updated `_compute_name` to render "Placeholder - {Product}" for untracked product
  placeholders.
- Updated `stock.lot._create_stock_rental_lot` to pass `product_id` when creating
  placeholder slots.
- Updated `sale.order.line._generate_stock_rental_lot` to pass `product_id` in all
  `stock.rental.slot` create calls.
- Added `product.product._generate_stock_rental_lot` method that deletes existing
  placeholder slots and creates one per `qty_available` for untracked storable rental
  products.
- Extended `stock.quant._generate_stock_rental_lot` to call
  `product.product._generate_stock_rental_lot` for untracked rental products on create,
  write, and unlink.
- Updated `post_init_hook` to generate placeholder slots for existing untracked rental
  products.
- Updated `wizard/stock_rental_slot_period.action_adjust_period` to include untracked
  product placeholders in date updates.
- Fixed missing `product_product` import in `models/__init__.py` and added explicit
  `stock_rental_slot_ids` One2many on `product.product`.
- Created demo data: Added "Rental Chair" product (storable, untracked, rentable) with 5
  units in inventory.
- Verified functionality via Odoo shell: placeholder slots are correctly created,
  updated, and deleted based on stock quant changes for untracked products.
- Updated existing test `test_slot_stock_sync.py` to pass `product_id` where slots are
  created directly.

## WIP

Author asked to add a smart button on the product form to show rental slots. Created
`views/product_product_views.xml` inheriting `product_normal_form_view` but got XML ID
validation error:

```
AssertionError: The ID reference "product_normal_form_view.inherit.rental_slots" must contain...
```

Next step: fix the view XML ID to not use dots other than module separation, then update
module and verify button appears on product form.

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
