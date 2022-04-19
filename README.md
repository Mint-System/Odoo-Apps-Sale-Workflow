# Odoo Apps: Sale Workflow

Collection of sale model related modules.

## Usage

Clone module into Odoo addon directory.

```bash
git clone git@github.com:mint-system/odoo-apps-sale-workflow.git ./addons/sale_workflow
```

## Available modules

| Module                                                                                            | Summary                                                                        |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [sale_order_line_date_propagate](sale_order_line_date_propagate/)                                 | This module ensures that line order dates are propagated to stock pickings.    |
| [sale_blanket_order_notes](sale_blanket_order_notes/)                                             | Notes for sale blanket and sale orders.                                        |
| [sale_order_notes](sale_order_notes/)                                                             | Notes for sale orders.                                                         |
| [sale_order_line_position](sale_order_line_position/)                                             | Use sale order line position for linked delivery orders and outgoing invoices. |
| [sale_order_default_commitment_date](sale_order_default_commitment_date/)                         | Default vaule for the commitment date on sale order.                           |
| [sale_order_contact_person](sale_order_contact_person/)                                           | Set contact person on sale order.                                              |
| [sale_order_delivery_note](sale_order_delivery_note/)                                             | Add note that is printed on sale order and delivery slip report.               |
| [sale_blanket_order_contact_person](sale_blanket_order_contact_person/)                           | Set contact person on sale order.                                              |
| [sale_blanket_order_send](sale_blanket_order_send/)                                               | Workflow with send blanket order by e-mail.                                    |
| [sale_order_line_default_packaging](sale_order_line_default_packaging/)                           | Sets the first packaging of the product as default.                            |
| [sale_order_default_carrier](sale_order_default_carrier/)                                         | Set sale order carrier from partner.                                           |
| [sale_blanket_order_comment](sale_blanket_order_comment/)                                         | Comment field for sale and blanket order.                                      |
| [sale_order_expected_commitment_date](sale_order_expected_commitment_date/)                       | If empty set commitment date equal to expected date.                           |
| [sale_order_line_description_name](sale_order_line_description_name/)                             | Use product name without default code if sale description is not set.          |
| [sale_blanket_order_crm_tags](sale_blanket_order_crm_tags/)                                       | Add CRM tags to sale blanket order.                                            |
| [sale_blanket_order_date_confirmed](sale_blanket_order_date_confirmed/)                           | Set confirmation date on sale blanket order.                                   |
| [sale_blanket_order_cancel_state](sale_blanket_order_cancel_state/)                               | Adds a cancel state to sale blanket order.                                     |
| [sale_blanket_order_invoice_shippinging_partner](sale_blanket_order_invoice_shippinging_partner/) | Set invoice and shipping partner on sale order.                                |
