from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # def _create_invoices(self, sale_orders):
    #     res = super()._create_invoices(sale_orders)
    #     for order_id in sale_orders:
    #         lines_with_temp_price = order_id.order_line.filtered(
    #             lambda l: l.temp_price_unit > 0 and l.qty_invoiced == l.product_uom_qty
    #         )
    #         if lines_with_temp_price:
    #             lines_with_temp_price.reset_temp_price()
    #             order_id.message_post(
    #                 body=_("Reset temporary prices and restored original prices."),
    #                 type="notification",
    #             )
    #     return res
