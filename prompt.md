---
title: "Set colors for slots gant view"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-20
harness: pi
model: deepseek-v4-flash-0731
input_tokens: 5047388
output_tokens: 147051
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

Badges & limits (author feedback):

- slot list view: `limit="100"` (100 records per page by default)
- `sale.order.rental_status` badge in the rental order list (`rental_order_view_tree`)
  now uses the palette via a new computed `rental_status_color` on `sale.order`
  (bootstrap decorations removed): draft/sent/False -> 10 green, pickup -> 5 purple,
  return -> 2 orange, returned/cancel -> 0 gray
- `sale.order.line.rental_status` in the rental form order-line list is now a colored
  badge via new computed `rental_status_color` on the line (same palette map;
  sent/cancel -> False -> green)
- kanban (`rental_order_view_kanban`): card `<kanban color="rental_status_color">` adds
  a colored strip per status, and the `rental_status` pill in the card footer switched
  from `label_selection` (green/orange/gray bootstrap) to `widget="badge"` +
  `color_field` for the palette colors; the base `state` pill stays unchanged
- DEPLOYED: `task update-module 19.0 ...` for both addons (exit 0); verified via
  fresh-boot `get_combined_arch` that list + kanban overrides are merged in DB. Odoo
  container was NOT running -> start with `task start odoo` to see colors. (Load
  warning: `sale.order.line.rental_status` selection override; could use `selection_add`
  later.)
- the earlier "show 100 in gantt" request was NOT implemented (only the list limit was
  confirmed); gantt paging defaults to all records

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

Completed on 2026-10-20 after author verification: colors for slot gantt/list/form,
order-level list + kanban badges, `limit="100"`, draft support, dev-only
verification fields all deployed and confirmed by the author (`task update-module`
ran, odoo container started, colors visible). The duplicate `super().action_cancel()`
fix remains a separate follow-up.
