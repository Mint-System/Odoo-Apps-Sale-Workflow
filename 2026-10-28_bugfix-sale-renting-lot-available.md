---
commit_ref:
title: "Bugfix Sale Renting Lot Available"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: draft
date_completed: YYYY-MM-DD
harness:
model:
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

Ensure that users in group `sales_team.group_sale_salesman` have full access on the slot model.

### Lot 0 does not remove placeholder slot

If qty for a `stock.lot` is set to 0.0 it should remove the placeholder slots.

### Rental status false color

If the rental status is false (which is the case for placeholder slots) it should be in a grey color.

### Rental slots without lot

This is a bigger task. If the rental product is tracked but only with qty the module should generate rental slots based on the stock qty of this product.

Create a `_create_stock_rental_lot` method for `product.product`. Show the slots as smart buttons on product (similar to stock.lot).

Changing the qty in stock should regenerate the slots.

### Testing

Write tests for the functionality.

Prepare the Odoo enviroment for testing.

I will test if the rental flow works with qty and serial tracked products in the same order.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness and model. If you have access to session info also add token count.
