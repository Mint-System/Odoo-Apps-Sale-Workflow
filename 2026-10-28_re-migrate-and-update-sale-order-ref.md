---
commit_ref: 18fd494c038955a68b8b34f421170e6d068e0d46
title: "Re-migrate and update sale order ref"
author: "Janik von Rotz <login@janikvonrotz.ch>"
action: implement
state: completed
date_completed: 2026-10-29
harness: pi
model: moonshotai/Kimi-K2.6
input_tokens: 1385
output_tokens: 334
---

# Re-migrate and update sale order ref

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

This is about the module `sale_order_ref`. There are 3 topics.

### 1. The module has been updated on 17.0 re-migrate the module.

There is a guide that explains how this is done:
https://wiki.mint-system.ch/prozesse-odoo-modul-migration/?h=prozesse+modul+#modul-migrieren

Do not run any prompts or commit anything. Do not create feature branch or PR.

### 2. Update search filter on sale order

Add `ref` to field `name` in `sale.view_sales_order_filter`.

### 3. Make `sale_renting_line_period` depend on `sale_order_ref` and update search filter.

Add `ref` to field `name` in `sale_renting.rental_order_view_search`.

@Clanker When task is completed set frontmatter state to review. Prompt the author to
verify the results.

## Worklog

### Completed tasks

1. **Re-migrated `sale_order_ref` from 17.0 to 19.0**
   - The 17.0 branch had additional features not present in the 19.0 version. Ported the
     following files and changes:
   - Added `data/system_parameters.xml` with default
     `sale_order_ref.displayname_template` config parameter.
   - Added `views/res_config_settings_views.xml` to configure the display name template
     in Sale settings.
   - Added `models/res_config_settings.py` with `sale_order_ref_displayname_template`
     and live preview fields.
   - Updated `models/sale_order.py` to use the template-based display name logic (with
     `display_name_formatted` method) instead of the hardcoded format.
   - Updated `models/__init__.py` to import the new settings model.
   - Created `tests/TEST_INSTRUCTIONS.rst`.
   - Updated `__manifest__.py` to include the new data and view files.

2. **Updated search filter on sale order**
   - Added inheritance record `view_sales_order_filter` in
     `sale_order_ref/views/sale_order_views.xml`
   - The `name` field's `filter_domain` now includes `('ref', 'ilike', self)` so
     searching by ref works in the sale order search view.

3. **Made `sale_renting_line_period` depend on `sale_order_ref` and updated search
   filter**
   - Added `sale_order_ref` to `depends` in `sale_renting_line_period/__manifest__.py`.
   - Added inheritance record `rental_order_view_search` in
     `sale_renting_line_period/views/sale_order_views.xml`
   - The `name` field's `filter_domain` now includes `('ref', 'ilike', self)` so
     searching by ref works in the rental order search view.

### Files changed

- `addons/sale_workflow/sale_order_ref/__manifest__.py`
- `addons/sale_workflow/sale_order_ref/models/sale_order.py`
- `addons/sale_workflow/sale_order_ref/models/__init__.py`
- `addons/sale_workflow/sale_order_ref/models/res_config_settings.py` (new)
- `addons/sale_workflow/sale_order_ref/data/system_parameters.xml` (new)
- `addons/sale_workflow/sale_order_ref/views/res_config_settings_views.xml` (new)
- `addons/sale_workflow/sale_order_ref/views/sale_order_views.xml`
- `addons/sale_workflow/sale_order_ref/tests/TEST_INSTRUCTIONS.rst` (new)
- `addons/sale_workflow/sale_renting_line_period/__manifest__.py`
- `addons/sale_workflow/sale_renting_line_period/views/sale_order_views.xml`

---

@Clanker If author confirms results set frontmatter state to completed, otherwise to
aborted. Update date, harness and model. If you have access to session info also add
token count.
