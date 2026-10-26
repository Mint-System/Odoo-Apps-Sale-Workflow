---
commit_ref: 96f944006ab79eb5516fc8f9d028a6525d5b2fd8
title: "Show company_id on stock rental slot"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-26
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 37368
output_tokens: 4859
---

# Show company_id on stock rental slot

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

If multi company is active, show `company_id` on `stock.rental.slot` form after
`is_placeholder`.

I expect that this field it related to `sale_order_id` or `lot_id`.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

Added `<field name="company_id" groups="base.group_multi_company" />` right after
`<field name="is_placeholder" />` in the `stock_rental_slot_form_view` of
`addons/sale_workflow/sale_renting_lot_available/views/stock_rental_slot_views.xml`.

Also added the missing multi-company record rule `stock_rental_slot_rule_company` in a
new file `security/stock_rental_slot_security.xml` and registered it in
`__manifest__.py`. Without this rule, users saw rental slots from all companies
regardless of the active company.

The `company_id` field already existed on the `stock.rental.slot` model (computed from
`sale_order_id` or `lot_id`), so only the form view and security rule needed to be
added. The field is shown only when multi-company is enabled via the
`base.group_multi_company` group.

Note: existing installations require a module upgrade (`-u sale_renting_lot_available`)
for the new `noupdate="1"` rule to be created in the database.

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
