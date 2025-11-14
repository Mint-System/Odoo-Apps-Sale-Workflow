# Odoo Apps: Sale Workflow

Odoo modules extending the `sale` module.

## Usage

Clone this repo into the Odoo addons directory.

```bash
git clone git@github.com:Mint-System/Odoo-Apps-Sale-Workflow.git ./addons/sale_workflow
```

## Available modules

| Module | Summary |
| --- | --- |
| [industry_fsm_sale_default_task](industry_fsm_sale_default_task) |         Additional sale order lines will be linked with field service project task. |
| [sale_blanket_order_cancel_state](sale_blanket_order_cancel_state) |         Adds a cancel state to sale blanket order. |
| [sale_blanket_order_carrier](sale_blanket_order_carrier) |         Set carrier on sale blanket order. |
| [sale_blanket_order_comment](sale_blanket_order_comment) |         Comment field for sale blanket order. |
| [sale_blanket_order_commitment_date](sale_blanket_order_commitment_date) |         Copies the blanket order line scheduled date to sale line commitment date. |
| [sale_blanket_order_contact_person](sale_blanket_order_contact_person) |         Set contact person on blanket order. |
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
| [sale_expense_link](sale_expense_link) |         Link expense and sale order line. |
| [sale_expense_unlink](sale_expense_unlink) |         Allow deletion of sale order expense lines. |
| [sale_order_comment](sale_order_comment) |         Comment field for sale order. |
| [sale_order_default_carrier](sale_order_default_carrier) |         Set sale order carrier from partner. |
| [sale_order_invoice_shipping_partner_restrict](sale_order_invoice_shipping_partner_restrict) |         Apply valid invoice and shipping addresses only. |
| [sale_order_line_date_propagate](sale_order_line_date_propagate) |         This module ensures that line order dates are propagated to stock pickings. |
| [sale_order_line_description_name](sale_order_line_description_name) |         Use product name without default code in sale order line. |
| [sale_order_line_form_action](sale_order_line_form_action) |         Adds a button to open a sale order line in the form view. |
| [sale_order_line_name_get](sale_order_line_name_get) |         Use product name in sale order display name before description. |
| [sale_order_line_position](sale_order_line_position) |         Show position numbers on sale order lines. |
| [sale_order_line_pricelist_fixed_discount](sale_order_line_pricelist_fixed_discount) |         Add discount from pricelist with fixed price. |
| [sale_order_line_temporary_price](sale_order_line_temporary_price) |         Custom unit price valid for first invoice. |
| [sale_order_notes](sale_order_notes) |         Notes for sale orders. |
| [sale_order_partner_membership](sale_order_partner_membership) |         Set membership address on sale order. |
| [sale_order_partner_pricelist](sale_order_partner_pricelist) |         Grant pricelist access with sale order. |
| [sale_order_partner_ref](sale_order_partner_ref) |         Show and filter the customer ref in sale order list. |
| [sale_order_sale_partner](sale_order_sale_partner) |         Set sale contact on sales order. |
| [sale_order_template_notes](sale_order_template_notes) |         Set notes on sale order templates. |
| [sale_partner_shipping_group](sale_partner_shipping_group) |         Access group for shipping address on sale orders and invoices. |
| [sale_project_key](sale_project_key) |         Show project key on sale order. |
| [sale_project_link](sale_project_link) |         Select existing project for sale quote. |
| [sale_subscription_disable_tokenization](sale_subscription_disable_tokenization) |         Do not force payment tokenization for order with subscriptions. |
| [sale_subscription_partner_pricelist](sale_subscription_partner_pricelist) |         Grant pricelist access with sale subscription. |
| [sale_subscription_period_discount](sale_subscription_period_discount) |         Apply discounts on subscription periods. |
