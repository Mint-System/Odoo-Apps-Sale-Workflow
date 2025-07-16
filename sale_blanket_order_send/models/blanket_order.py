import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class BlanketOrder(models.Model):
    _inherit = ["sale.blanket.order"]

    state = fields.Selection(selection_add=[("sent", "Sent"), ("open",)], ondelete={"sent": "cascade"})

    # Generate name from sequence on create
    @api.model
    def create(self, vals):
        if vals.get("name", _("Draft")) == _("Draft"):
            sequence_obj = self.env["ir.sequence"]
            if self.company_id:
                sequence_obj = sequence_obj.with_company(self.company_id.id)
            vals["name"] = sequence_obj.next_by_code("sale.blanket.order")

        return super().create(vals)

    # Do not generate name from sequence on confirm
    def action_confirm(self):
        self._validate()
        for order in self:
            order.write(
                {
                    "confirmed": True,
                    "date_confirmed": fields.Datetime.now(),
                }
            )
        return True

    def action_order_send(self):
        # Opens a wizard to compose an email, with relevant mail template loaded by default
        self.ensure_one()
        self.env.context.get("lang")
        ir_model_data = self.env["ir.model.data"]
        template_id = ir_model_data.check_object_reference(
            "sale_blanket_order_send", "email_template_sale_blanket_order"
        )[1]
        template = self.env["mail.template"].browse(template_id)
        if template.lang:
            template._render_lang(self.ids)[self.id]
        ctx = {
            "default_model": "sale.blanket.order",
            "active_model": "sale.blanket.order",
            "default_res_id": self.ids[0],
            "active_id": self.ids[0],
            "default_use_template": bool(template_id),
            "default_template_id": template_id,
            "default_composition_mode": "comment",
            "mark_bo_as_sent": True,
            "force_email": True,
        }
        compose_form_id = ir_model_data.check_object_reference("mail", "email_compose_message_wizard_form")[1]
        return {
            "name": _("Compose Email"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form_id, "form")],
            "view_id": compose_form_id,
            "target": "new",
            "context": ctx,
        }

    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get("mark_bo_as_sent"):
            self.filtered(lambda o: o.state == "draft").with_context(tracking_disable=True).write({"state": "sent"})
        return super(BlanketOrder, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
