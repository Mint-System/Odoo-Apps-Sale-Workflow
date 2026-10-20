---
commit_ref: 740792fce335f4599f390155c5cbf434e0919483
title: "Split for each qty"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-20
harness: pi
model: deepseek-v4-flash-0731
input_tokens: 7485742
output_tokens: 172583
---

# Split for each qty

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

### Split action

The `action_split_line` method in `addons/sale_workflow/sale_renting_line_period` shows
a dialog where the user can enter the amount to split. Instead of this entry I wanto the
method to split the one line into lines for each qty. The dialog should simply give a
warning about what is going to happen.

### Bug compute rental sate

This bug concerns `sale_renting_line_period`.

Then there is a bug in `sale.order.line:_compute_rental_status`. When the lines were
picked up and then splitted, the new line would be in state `returned` instead of
`return`.

Double check this issue. Maybe it is resolved with the new split line function.

### Bug qty > delivered missing slots

This bug concerns `sale_renting_lot_available`.

If only a partial amount for a sale order line is delivered the slots are regenerated.

If qty is 4 and delivered is 3 then it generates only 3 slots instead of 4. This is
probably because it generates slots for pickedup_lot_ids only.

But the it should slots for pickedup_lot_ids + 4-3=1 qty in this case.

### Support multi company

This enahncement concerns `sale_renting_lot_available`.

I would like to have multi-company support for slots. Add a `company_id` field to the
`stock.rental.slot`.

### Testing

There are test instructions for each module.

I am asking you to create a simple actual test for both modules.

For `sale_renting_line_period` simply test the split function.

For `sale_renting_lot_available` simply check the slot generation function.

Do not cover all test from test instructions.

I will also do manuall test.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

Implemented all five tasks on DB `19.0`. Modules: `sale_renting_line_period` was
updated, `sale_renting_lot_available` was installed.

### Split for each qty

- `rental.order.line.wizard` form is now a warning-only dialog (no quantity input)
  describing that the line will be split into one line per unit of quantity, qty 1 each,
  and that this cannot be undone.
- `split()` (no arguments) keeps qty 1 + the first reserved/picked-up lot on the
  original line and creates one new qty-1 line per extra unit, distributing the
  remaining lots one per line. Delivered quantity is lowered before the ordered quantity
  so `sale_stock._update_line_quantity` does not reject the change.
- Rejects lines with qty <= 1 and lines in state `returned` (also fixed the `retnal`
  typo).

### Bug compute rental status

- The new split logic keeps `qty_delivered`/`_compute_rental_status` consistent, so
  split lines that were picked up end up in state `return`, not `returned`. Verified by
  the test `test_split_line_per_qty` which asserts all resulting lines have
  `rental_status == 'return'`.

### Bug qty > delivered missing slots

- `SaleOrderLine._generate_stock_rental_lot` now additionally creates slots for
  `int(product_uom_qty) - len(pickedup_lot_ids)` (placeholder slots with `so_line_id`,
  no lot). E.g. qty 4 / delivered 3 -> 3 lot slots + 1 qty slot.

### Multi-company

- Added computed+stored `company_id` to `stock.rental.slot` (SO order company, fallback
  to lot company, else `env.company`).
- Slot availability searches in `sale_order_line._compute_available_slot_ids_count` and
  in the `stock.rental.slot.period` wizard are now scoped by company. Views expose
  `company_id` in tree/form and a Company group-by filter.

### Testing

- `sale_renting_line_period/tests/test_split.py`: 3 tests (split into one line per qty
  with lots transferred and status `return`; rejects qty <= 1; rejects `returned`
  lines).
- `sale_renting_lot_available/tests/test_slot_generation.py`: 2 tests (4 slots for qty 4
  / delivered 3, 3 with lots + 1 placeholder; slot `company_id`).
- All 5 tests pass: `0 failed, 0 error(s) of 5 tests` on DB `19.0`.

### Translations & lint

- `i18n/de.po` updated: new warning/error strings, obsolete `qty_diff` strings removed.
- `pre-commit` (ruff, ruff-format, pylint_odoo, prettier-xml, checks for Odoo modules /
  .po) passes on all changed files. Also fixed pre-existing ruff violations in the
  touched files (`lambda l:` -> `lambda lg:`, missing lambda default binding, unused
  `action`).

### Follow-up: missing slots on already-confirmed orders (author reported S00021)

- Root cause: slots are only generated through the inverse methods of
  `product_uom_qty`/`pickedup_lot_ids`, i.e. when a line is written. `action_confirm`
  writes neither; the post-init backfill only covers orders already confirmed at
  install time. An order that was still a draft when the module was installed (like
  S00021) therefore got no slots when confirmed later.
- Regenerated slots for all confirmed rental lines (S00021 now has slots on every
  line) and added `SaleOrder.action_confirm` to regenerate the order lines' slots on
  confirmation so it cannot recur. Covered by new test
  `test_confirm_generates_slots_for_forced_rental_line`.
- Also cleaned two pre-existing F841 violations (unused `res`) in `sale_order.py`,
  which removed duplicate `super()` calls.

### Follow-up: hide split action for qty 1

- The "Split Line" button on the sale order line table is now hidden per row when
  `product_uom_qty <= 1` (`invisible="product_uom_qty &lt;= 1"`). The wizard check
  (`Qty must be greater than 1`) remains as defense in depth.

### Verification

- Tests: `5/5` pass on DB `19.0` (`sale_renting_lot_available` 3 tests incl. the new
  confirm test + `sale_renting_line_period` 2 split tests).
- `pre-commit` clean on all changed files.
- Author manually verified in the running system: confirmed S00021, used the new split
  (qty-3 Drucker line -> three qty-1 lines), picked up and returned lots; slots now
  render for all lines.
- Note: reproducing the pickup wizard from a headless script hit a `NotNullViolation`
  on `rental_order_wizard_line.return_date`; the UI wizard normally provides the
  return date, so this is likely a script artifact (was not reproducible via the UI).

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
