---
title: "Set colors for slots gant view"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: review
date_completed: 2026-10-20
harness: pi
model: deepseek-v4-flash-0731
input_tokens: 678855
output_tokens: 25728
---

# Set colors for slots gant view

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I would like to set specific colors for `rental_state` in
`addons/sale_workflow/sale_renting_lot_available/models/stock_rental_slot.py` for the
gantt view.

The current choice would be:

False: #1dff4b pickup: #740079 return: #f47910 returned: #5e615e

Odoo has an index of colors. If color can not be set as suggested, try to find a
matching index color.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

Set per-status colors on `stock.rental.slot` (gantt pills, list badges, form).

The gantt `color` attribute and the list/form badge widget only support integer indices
into the first 12 `$o-colors` colors: the gantt JS applies
`getColorIndex(value) = value % 12` and the badge CSS only defines
`o_badge_color_0..11`. Verified against `web_gantt/gantt_helpers.js` and
`web/static/src/core/badge/badge.scss`. Therefore a single computed field
`rental_status_color` maps each `rental_status` to its closest 0-11 index:

- False #1dff4b (bright green) -> 10 (#61c36e)
- pickup #740079 (purple) -> 5 (#9f628f)
- return #f47910 (orange) -> 2 (#dc8534)
- returned #5e615e (grey) -> 0 (#a2a2a2)

(Gantt previous indices 47/17/2/29 were wrong: `% 12` collapsed 17 and 29 both to index
5 (mauve). Note: `% 12` also collapses any 0-11 input.)

Views:

- gantt `color="rental_status_color"`
- list `rental_status` rendered with `widget="badge"` + `color_field`, showing the
  colored badge (decorations removed)
- form shows the status as colored badge plus a `rental_status_color_hex` badge (palette
  hex on a colored pill, `color_field` on the integer) and the plain
  `rental_status_color` integer. Both verification fields carry
  `groups="base.group_no_one"` (developer mode only); the status badge itself stays
  visible to everyone

Verified against the live `19.0` DB via `odoo shell` (slots of S00021):

- Drucker/qty-1 line (qty_delivered==qty_returned==1) -> status `returned`, color 0, hex
  #a2a2a2 -> the reported "rental_color 0" is correct
- qty-3 line (qty_returned 0 < qty_delivered 3) -> status `return`, color 2, hex #dc8534
  (orange)

Additionally (feedback): `action_create_order` now opens the rental order form
`sale_renting.rental_order_primary_form_view` instead of the default
`sale.view_order_form`.

Draft support (author feedback):

- `sale_renting_line_period/_compute_rental_status` now treats any order that is not
  confirmed (`line.state != "sale"`, i.e. draft/sent/cancelled) like a non-rental line:
  `rental_status = False` (was: still computed from the delivered/returned quantities).
  Verified live: S00023 (draft) line 49 now computes `False` instead of `returned`.
- `stock.rental.slot.rental_status` was a stored related, so existing draft slots kept
  stale values (the source is a non-stored compute, nothing triggered a refresh).
  Removed `store=True` so the slot always mirrors the line's live status. Verified live:
  S00023 slots 89/90 now show status empty, color 10 (#61c36e green) like `False`.

Open (not yet applied, awaiting author): `sale_renting_line_period` `action_cancel`
calls `super().action_cancel()` twice.

Awaiting author verification. If confirmed, state -> completed, otherwise aborted.
