import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class BlanketOrderWizard(models.TransientModel):
    _inherit = "sale.blanket.order.wizard"

    def _prepare_so_line_vals(self, line):
        res = super()._prepare_so_line_vals(line)
        res.update({"discount": line.discount})
        return res

    @api.model
    def _default_lines_discount(self):
        blanket_order_line_obj = self.env["sale.blanket.order.line"]
        blanket_order_line_ids = self.env.context.get("active_ids", False)
        active_model = self.env.context.get("active_model", False)

        if active_model == "sale.blanket.order":
            bo_lines = self._default_order().line_ids
        else:
            bo_lines = blanket_order_line_obj.browse(blanket_order_line_ids)

        self._check_valid_blanket_order_line(bo_lines)

        lines = [
            (
                0,
                0,
                {
                    "blanket_line_id": bol.id,
                    "product_id": bol.product_id.id,
                    "date_schedule": bol.date_schedule,
                    "remaining_uom_qty": bol.remaining_uom_qty,
                    "price_unit": bol.price_unit,
                    "product_uom": bol.product_uom,
                    "qty": bol.remaining_uom_qty,
                    "partner_id": bol.partner_id,
                    "discount": bol.discount,
                },
            )
            for bol in bo_lines.filtered(lambda l: l.remaining_uom_qty != 0.0)
        ]
        return lines

    """"OVERWRITE: include discount"""
    line_ids = fields.One2many(
        "sale.blanket.order.wizard.line",
        "wizard_id",
        string="Lines",
        default=_default_lines_discount,
    )


class BlanketOrderWizardLine(models.TransientModel):
    _inherit = "sale.blanket.order.wizard.line"

    discount = fields.Float(string="Discount (%)", digits="Discount", default=0.0)
