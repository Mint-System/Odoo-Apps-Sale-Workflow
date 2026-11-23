---
commit_ref: 0438d36def2dfccf9044f7a22d391cbdc744e3de
title: "Improvements for sale renting modules"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-11-11
harness: pi
provider: deepseek
model: deepseek-v4-1-flash-1017
input_tokens: 619349
output_tokens: 73766
---

# Improvements for sale renting modules

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Read entire task section and prepare a list of todos
- Update the todo list while working on task

## Task

I want you to improve the `sale_renting_line_period` and `sale_renting_lot_available` modules.

### Rental return datetime

The rental return datetime field must always set `23:59:59` (max time) as default time.

I was not possible to change the field to date type. So this is a workaround.

Update the `_compute_rental_period` method.

### Split sale order line not working

When I have a rental order with a deliverd line and want to split it, I get this error message:

> Die bestellte Menge einer Verkaufsauftragszeile kann nicht unter die bereits gelieferte Menge gesetzt werden. Legen Sie stattdessen eine Retoure in Ihrem Bestand an.

Try to reproduce this issue:

- reserved_lot_ids: set 8 lots
- pickedup_lot_ids: set 8 lots
- returned_lot_ids: 0
- product_uom_qty: 8
- qty_deliverd: 8
- qty_returned: 0 

My assumption is that `split()` in `addons/sale_workflow/sale_renting_line_period/wizard/rental_order_line_wizard.py` needs a fix.

### Check availability with non overlapping slots

The `get_available_slot_ids` in `addons/sale_workflow/sale_renting_lot_available/wizard/stock_rental_slot_period.py`  basically gets the non-placeholder slots that touch the boundaries of `end_date`  and `start_date`, counts them and returns count of placeholder slots minus the counted non-placeholder slots.

Now there is a problem with this simple approach. Assume with this setup:

We have a product with:

- placeholder slots: 5

Then we slot 1:

- start_date: 2026-12-01
- end_date: 2027-02-01

Then we slot 2:

- start_date: 2026-12-01
- end_date: 2027-08-31

Then we slot 3:

- start_date:  2027-07-01
- end_date: 2027-08-31

And then we check this date:

- start_date: 2027-01-01
- end_date: 2027-07-31

With the current setup the result of available slots is 5 - 3 = 2. Because all of the slots touch the boundaries.

But the correct result is 5 - 2 = 3. Because slot 3 starts after slot 2 ends. So these slots do not overlap.

I think soliving this issue requires a more sophisticated check. I think I need to know which slots do overlap in the time range which do not.

An new formular got get the available slots could be: placeholder sots - slots in boundaries + amount of slot pairs that do not overlap.

Instead of implementing this righ away please provide an approach on how to solve this problem.

@Clanker When task is completed set frontmatter state to review. Prompt the author to verify the results.

## Worklog

### Rental return datetime

The return date is a datetime field that is displayed as a date. Instead of
converting it to a date field, the time is forced to the last second of the day.

- `sale_renting_line_period/models/sale_order_line.py`: new `_get_rental_return_date`
  helper; `_compute_rental_period` uses it for the line return date. Returned lines
  keep their own return date.

The datetime is stored in UTC but the day is defined by the user timezone. The helper
converts the timestamp to the user timezone, sets the time to `datetime.time.max` of
that calendar day and converts it back to UTC:

```python
user_tz = self.env.tz
local_return_date = UTC.localize(return_date).astimezone(user_tz)
max_return_date = datetime.combine(local_return_date.date(), time.max)
return user_tz.localize(max_return_date).astimezone(UTC).replace(tzinfo=None, microsecond=0)
```

The microseconds are dropped because the slot periods are compared by second. For
`Europe/Zurich` a return date of `2026-12-05 18:00 UTC` becomes `2026-12-05 22:59:59 UTC`,
which is `23:59:59` local time.

### Split sale order line

Root cause: `sale_stock` compares the new `product_uom_qty` against the delivered
quantity stored in the database. Reducing `qty_delivered` in the same `write()` as
`product_uom_qty` is too late, so the split was rejected with "The ordered quantity
of a sale order line cannot be decreased below the amount already delivered".

- `sale_renting_line_period/wizard/rental_order_line_wizard.py`: first write reduces
  `qty_delivered` and `qty_returned` to at most one unit, second write assigns the
  first lot of `reserved_lot_ids`, `pickedup_lot_ids`, `returned_lot_ids` and sets
  `product_uom_qty` to 1.0. The remaining units are copied one by one, each with its
  own lot and a per-line delivered/returned quantity.

### Check availability

Approach: the number of items that can be rented in a period is limited by the
maximum number of bookings that overlap *at the same time*, not by the number of
bookings that touch the period boundaries.

1. Collect the booked slots of the product that intersect the requested period.
2. Build a sweep line over the slot start and return dates: `+1` on start, `-1` on
   return. Sort by date and process ends before starts, so slots that only touch at
   a boundary do not count as overlapping.
3. The running maximum of the sweep is the number of blocked items.
4. Available slots = placeholder slots - blocked items.

This is O(n log n) and does not need the pairwise comparison from the proposed
formula (placeholder slots - slots in boundaries + non-overlapping pairs).

- `sale_renting_lot_available/models/stock_rental_slot.py`: new `_get_max_overlap`
  and `_get_available_placeholder_slot_ids` helpers.
- `sale_renting_lot_available/wizard/stock_rental_slot_period.py`: `get_available_slot_ids`
  uses the helper.
- `sale_renting_lot_available/models/sale_order_line.py`: `available_slot_ids_count`
  uses the same overlap logic and ignores the line's own slots.

### Tests

- `sale_renting_line_period/tests/test_rental_period.py`: return date is end of day,
  is calculated in the user timezone (including the day rollover), follows the order
  and stays untouched on returned lines.
- `sale_renting_line_period/tests/test_split.py`: split of a fully delivered line.
- `sale_renting_lot_available/tests/test_slot_availability.py`: overlap of
  non-overlapping bookings (5 - 2 = 3), fully overlapping bookings, bookings outside
  of the period.

All 20 module tests pass. `ruff format --check` passes; the remaining `ruff check`
warnings are pre-existing.

@Clanker If author confirms results set frontmatter state to completed, otherwise to aborted. Update date, harness, provider and model. If you have access to session info also add token count. Finally, update the changelog with the most important changes.
