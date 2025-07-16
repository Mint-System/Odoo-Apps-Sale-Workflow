import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
            for line in rec.order_line:
                line._set_default_task()
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _set_default_task(self, values=[]):
        """Search for first fsm line of sale order and use task as default."""
        if "task_id" not in values:
            for line in self.filtered(lambda l: not l.task_id and l.product_id.detailed_type in ["consu", "product"]):
                order_line_ids = self.order_id.order_line.filtered(lambda l: l.task_id.is_fsm)[:1]
                if order_line_ids:
                    line.write({"task_id": order_line_ids.task_id.id})

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines._set_default_task(vals_list)
        return lines

    def write(self, values):
        result = super().write(values)
        self._set_default_task(values)
        return result
