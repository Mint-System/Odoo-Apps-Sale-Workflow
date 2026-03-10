import logging
from datetime import date

from psycopg2 import IntegrityError, errorcodes

from odoo import _, api, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.constrains("order_line", "order_line.product_id", "order_line.product_uom_qty")
    def _check_only_one_permit_product(self):
        for order in self:
            permit_lines = order.order_line.filtered(
                lambda l: l.product_id.product_tmpl_id.duration and l.product_uom_qty > 0
            )

            if len(permit_lines) > 1:
                raise ValidationError(_("Sie können nur ein Patent pro Bestellung haben."))

            if any(l.product_uom_qty > 1 for l in permit_lines):
                raise ValidationError(_("Sie können max. 1 Einheit eines Patents pro Bestellung haben."))

    def _assign_permit_number(self):
        self.ensure_one()

        partner = self.partner_id
        if not partner or partner.permit_number:
            return

        seq = self.env.ref("sale_order_permit.seq_permit_number")

        attempts = 0
        while attempts < 300:
            attempts += 1

            number = seq.next_by_id()

            try:
                with self.env.cr.savepoint():
                    partner.permit_number = number

                    # force SQL
                    self.env["res.partner"].flush_model(["permit_number"])

                return

            except IntegrityError as e:
                if getattr(e, "pgcode", None) != errorcodes.UNIQUE_VIOLATION:
                    raise
                # duplicate → retry with a NEW number
                continue

        raise RuntimeError("Could not generate a unique permit number for partner %s" % partner.display_name)


    def action_confirm(self):
        # no sale order if date is after March 31
        today = date.today()
        limit_date = date(today.year, 3, 31)

        for order in self:
            product = order.order_line[0].product_id
            for line in order.order_line:
                if product.duration == "year" and line.date_from and line.date_from > limit_date:
                    raise ValidationError(_("Sie können kein Jahrespatent mehr nach dem (%s) kaufen.") % limit_date)

        for order in self:
            product = order.order_line[0].product_id
            if not order.partner_id.permit_number and product.duration == "year":
                order._assign_permit_number()

        res = super().action_confirm()

        return res

    def _verify_updated_quantity(self, order_line, product_id, new_qty, **kwargs):
        new_qty, warning = super()._verify_updated_quantity(order_line, product_id, new_qty, **kwargs)

        self.ensure_one()

        product = self.env["product.product"].browse(product_id)
        tmpl = product.product_tmpl_id

        # Only apply the rule for permit products
        if not tmpl.duration:
            return new_qty, warning

        # Allow removing the line
        if new_qty <= 0:
            return new_qty, warning

        # quantity of a permit product is max 1
        if new_qty > 1:
            raise UserError(_("Sie können nur max. eine Einheit eines Patents im Warenkorb haben."))

        # only one duration product in the cart
        existing_permit_lines = self.order_line.filtered(
            lambda l: l.product_id.product_tmpl_id.duration
            and (not order_line or l.id != order_line.id)
            and l.product_uom_qty > 0
        )

        if existing_permit_lines:
            raise UserError(_("Sie können nur ein Patent im Warenkorb haben."))

        return new_qty, warning

    def _cart_update(self, product_id, line_id=None, add_qty=0, set_qty=0, **kwargs):
        res = super()._cart_update(product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)

        permit_lines = self.order_line.filtered(
            lambda l: l.product_id.product_tmpl_id.duration and l.product_uom_qty > 0
        )

        if len(permit_lines) > 1:
            raise UserError(_("Sie können nur ein Patent im Warenkorb haben."))

        if any(l.product_uom_qty > 1 for l in permit_lines):
            raise UserError(_("Sie können nur eine Einheit eines Patents in den Warenkorb legen."))

        return res
