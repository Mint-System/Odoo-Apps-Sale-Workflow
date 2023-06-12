# Odoo Apps: Sale Workflow

Collection of sale model related modules.

## Usage

Clone module into Odoo addon directory.

```bash
git clone git@github.com:mint-system/odoo-apps-sale-workflow.git ./addons/sale_workflow
```

## Available modules

| Module | Summary |
| --- | --- |
| [sale_blanket_order_cancel_state](sale_blanket_order_cancel_state) |         Adds a cancel state to sale blanket order. |
| [sale_blanket_order_carrier](sale_blanket_order_carrier) |         Set carrier on sale blanket order. |
| [sale_blanket_order_comment](sale_blanket_order_comment) |         Comment field for sale blanket order. |
| [sale_blanket_order_commitment_date](sale_blanket_order_commitment_date) |         Copies the blanket order line scheduled date to sale line commitment date. |
| [sale_blanket_order_contact_person](sale_blanket_order_contact_person) |         Set contact person on sale order. |
| [sale_blanket_order_crm_tags](sale_blanket_order_crm_tags) |         Add CRM tags to sale blanket order. |
| [sale_blanket_order_date_confirmed](sale_blanket_order_date_confirmed) |         Set confirmation date on sale blanket order. |
| [sale_blanket_order_discount](sale_blanket_order_discount) |         Define discount on sale blanket order line. |
| [sale_blanket_order_fiscal](sale_blanket_order_fiscal) |         Copy fiscal position from blanket to sale order. |
| [sale_blanket_order_invoice_shipping_partner](sale_blanket_order_invoice_shipping_partner) |         Set invoice and shipping partner on sale order. |
| [sale_blanket_order_line_description](sale_blanket_order_line_description) |         Copy description field of order lines to sale order. |
| [sale_blanket_order_notes](sale_blanket_order_notes) |         Notes for sale blanket and sale orders. |
| [sale_blanket_order_readonly_states_extended](sale_blanket_order_readonly_states_extended) |         Sets readonly states for other sale blanket order modules. |
| [sale_blanket_order_readonly_states](sale_blanket_order_readonly_states) |         Override readonly states. |
| [sale_blanket_order_reference](sale_blanket_order_reference) |         Copy customer reference from blanket to sale order. |
| [sale_blanket_order_send](sale_blanket_order_send) |         Send blanket order by e-mail. |
| [sale_blanket_order_stock_terms](sale_blanket_order_stock_terms) |         Set incoterm and shipping policy on blanket order. |
| [sale_blanket_order_template](sale_blanket_order_template) |         Setup sale blanket order template. |
| [sale_expense_link](sale_expense_link) |         Link expense ande sale order line. |
| [sale_expense_unlink](sale_expense_unlink) |         Allow deletion of sale order expense lines. |
| [sale_order_check_price](sale_order_check_price) |         Prevent sale order confirmation if line price is zero. |
| [sale_order_comment](sale_order_comment) |         Comment field for sale order. |
| [sale_order_contact_person](sale_order_contact_person) |         Set contact person on sale order. |
| [sale_order_default_carrier](sale_order_default_carrier) |         Set sale order carrier from partner. |
| [sale_order_default_commitment_date](sale_order_default_commitment_date) |         Default vaule for the commitment date on sale order. |
| [sale_order_delivery_note](sale_order_delivery_note) |         Add note that is printed on sale order and delivery slip report. |
| [sale_order_expected_commitment_date](sale_order_expected_commitment_date) |         If empty set commitment date equal to expected date. |
| [sale_order_line_date_propagate](sale_order_line_date_propagate) |         This module ensures that line order dates are propagated to stock pickings. |
| [sale_order_line_default_packaging](sale_order_line_default_packaging) |         Sets the first packaging of the product as default. |
| [sale_order_line_description_name](sale_order_line_description_name) |         Use product name without default code if sale description is not set. |
| [sale_order_line_name_get](sale_order_line_name_get) |         Use product name in sale order display name before description. |
| [sale_order_line_not_billable](sale_order_line_not_billable) |         Set product as not billable and ensure its filtered when invoicing the sale order. |
| [sale_order_line_pos](sale_order_line_pos) |         Use sale order line position for linked delivery orders and outgoing invoices. |
| [sale_order_line_pricelist_fixed_discount](sale_order_line_pricelist_fixed_discount) |         Add discount from pricelist with fixed price. |
| [sale_order_line_purchase_margin](sale_order_line_purchase_margin) |         Calculate sale line margin from linked purchase. |
| [sale_order_mrp_production_cancel](sale_order_mrp_production_cancel) |         Cancel linked manufacturing order when sale order is cancelled. |
| [sale_order_multi_pricelist](sale_order_multi_pricelist) |         Select partner pricelist based on order date. |
| [sale_order_notes](sale_order_notes) |         Notes for sale orders. |
| [sale_order_template_notes](sale_order_template_notes) |         Set notes on sale order templates. |
