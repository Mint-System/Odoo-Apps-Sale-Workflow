---
title: "Generate lot rental from stock lot"
state: completed
---

# Run 02

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I want to link the `stock.lot` with `stock.rental.lot`. When a `stock.lot` for a product
with `rent_ok` is created, then an entry `stock.rental.lot` must be created.

Create an inherited class with
`task generate-module-inherit addons/sale_workflow/sale_renting_lot_available stock.lot`

Add an action `_create_stock_rental_lot` that checks the `product_id.rent_ok` and
creates a `stock.rental.lot` entry. Call this action in a `create` method:

```python
@api.model_create_multi
def create(self, vals_list):
```

Then I want to link `sale.order.line` with `stock.rental.lot`. When a `sale.order.line`
with `is_rental` is created, then add an entry `stock.rental.lot`.

Create an inherited class with
`task generate-module-inherit addons/sale_workflow/sale_renting_lot_available sale.order.line`

Add an action `_create_stock_rental_lot` that checks `self.is_rental` and creaes a
`stock.rental.lot` entry. Call this action in a `create` method:

If the `sale.order.line` is unlinked, unlink all `sale.rental.lot` entries thare are
connected to the line.

If the `stock.lot` is archived, archive all `sale.rental.lot` entries. Add an `active`
field to `sale.rental.lot`.

Add an init hook the module that calls the `sale.order.line._create_stock_rental_lot()`
and the `stock.lot:_create_stock_rental_lot()` for all entries. This ensures that when
installing the modules lots are created for existing `stock.lot` and `sale.order.line`.

Once everything is ready I will install and test the module.

## Worklog

@Clanker Add a summary here once the task has been completed.

- Relaxed `required` constraints on `stock.lot.rental.lot_id` and `so_line_id` to allow
  entries being created from either parent independently, and added an `active` boolean
  field for archive propagation.
- Generated `models/stock_lot.py` inheriting `stock.lot` with
  `_create_stock_rental_lot()` that creates a `stock.lot.rental` entry when
  `product_id.rent_ok` is true, called from a `create()` override. Added a `write()`
  override that archives linked `stock.lot.rental` records when the lot itself is
  archived.
- Generated `models/sale_order_line.py` inheriting `sale.order.line` with
  `_create_stock_rental_lot()` that creates a `stock.lot.rental` entry when `is_rental`
  is true, called from a `create()` override. Added an `unlink()` override that removes
  linked `stock.lot.rental` records when the line is deleted.
- Implemented a `post_init_hook` in `__init__.py` that backfills `stock.lot.rental`
  entries for existing rentable lots and existing rental sale order lines on module
  install.
- Referenced `post_init_hook` in `__manifest__.py`.

@Clanker Set frontmatter state to completed.
