import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_name = fields.Char(inverse="_inverse_project_name")
    domain = fields.Char()
    consulting_partner_id = fields.Many2one("res.partner", domain="[('helm_product_ids','!=',False)]")
    cluster_id = fields.Many2one("kubectl.cluster")
    chart_ids = fields.One2many("helm.chart", compute="_compute_chart_ids")
    release_ids = fields.Many2many("helm.release", compute="_compute_release_ids", store=True)
    release_count = fields.Integer(string="Releases", compute="_compute_release_ids", store=True)

    @api.depends("order_line.product_id", "order_line.release_id")
    def _compute_release_ids(self):
        for order in self:
            order.release_ids = order.order_line.release_id
            order.release_count = len(order.order_line.release_id)

    def _compute_chart_ids(self):
        for rec in self:
            rec.chart_ids = rec.order_line.product_id.chart_id

    def _inverse_project_name(self):
        """
        Ensure project name is alphanumerical.
        """
        for rec in self:
            if rec.project_name:
                if not rec.project_name.isalnum():
                    raise ValidationError(_("Project name must only contain alphanumeric characters."))

    def action_confirm(self):
        """
        For each order line with a chart, install chart.
        """
        res = super().action_confirm()
        for order in self.filtered("chart_ids"):
            namespace_id = self.env["kubectl.namespace"].get_or_create(
                {"name": order.project_name, "cluster_id": order.cluster_id.id}
            )
            for line in order.order_line:
                release_id = line.product_id.chart_id.create_release(namespace_id, order.partner_id)
                line.release_id = release_id
                release_id._compute_values()
                release_id.action_install()
        return res

    def action_view_release(self):
        self.ensure_one()
        view_form_id = self.env.ref("helm.helm_release_form_view").id
        view_list_id = self.env.ref("helm.helm_release_list_view").id
        action = {
            "type": "ir.actions.act_window",
            "domain": [("id", "in", self.release_ids.ids)],
            "view_mode": "tree,form",
            "name": _("Releases"),
            "res_model": "helm.release",
        }
        if self.release_count == 1:
            action.update({"views": [(view_form_id, "form")], "res_id": self.release_ids.id})
        else:
            action["views"] = [(view_list_id, "tree"), (view_form_id, "form")]
        return action
