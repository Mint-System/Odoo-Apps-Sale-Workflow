from odoo import api, fields, models


class BlanketOrderLine(models.Model):
    _inherit = "sale.blanket.order.line"

    discount = fields.Float(string="Discount (%)", digits="Discount", default=0.0)

    @api.depends(
        "original_uom_qty",
        "price_unit",
        "taxes_id",
        "order_id.partner_id",
        "product_id",
        "currency_id",
        "discount",
    )
    def _compute_amount(self):
        for line in self:
            line.price_unit
            price_reduce = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.taxes_id.compute_all(
                price_reduce,
                line.currency_id,
                line.original_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_id,
            )
            line.update(
                {
                    "price_tax": sum(t.get("amount", 0.0) for t in taxes.get("taxes", [])),
                    "price_total": taxes["total_included"],
                    "price_subtotal": taxes["total_excluded"],
                }
            )
